"use client";

import { Fragment, useState } from "react";
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import {
  sanitizeInput,
  validateHealthcareQuery,
  detectDangerousPrompt
} from "@/lib/queryValidation";
import { Message, MessageContent } from "@/components/ai-elements/message";
import {
  PromptInput,
  PromptInputBody,
  type PromptInputMessage,
  PromptInputSubmit,
  PromptInputTextarea,
  PromptInputToolbar,
  PromptInputTools,
} from "@/components/ai-elements/prompt-input";
import { Response } from "@/components/ai-elements/response";
import { Loader } from "@/components/ai-elements/loader";
import { ChatStatus } from "ai";
import { ChatMessage } from "@/types/chat";
import {
  detectPromptInjection,
  detectUnsafeHealthcareQuery
} from "@/lib/security";

export default function RAGChatBot() {
  const [input, setInput] = useState("");
  const [inputError, setInputError] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<ChatStatus>("ready");

  const sendMessage = async (cleanedInput: string) => {

    // Add user message
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      parts: [
        {
          type: "text",
          text: cleanedInput
        }
      ],
      sources: []
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        body: JSON.stringify({
          messages: [...messages, userMessage]
        })
      });
      setStatus("streaming");
      const data = await response.json();
      setMessages((prev) => [...prev, data.messages[0]]);
      handleResponse("ready", "");
    } catch (e) {
      console.log("Failed", JSON.stringify(e));
      handleResponse("error", "Failed to get result.");
    }
  };

  const handleSubmit = (message: PromptInputMessage) => {
    setInput("");
    setInputError("");
    setStatus("submitted");

    // Handling validations
    const cleanedInput = sanitizeInput(input);
    const validationError = validateHealthcareQuery(cleanedInput);

    if (validationError) {
      handleResponse("error", validationError);
      return;
    }

    if (detectDangerousPrompt(cleanedInput)) {
      handleResponse("error", "Unsupported or unsafe query detected.");
      return;
    }

    if (detectPromptInjection(cleanedInput)) {
      handleResponse("error", "Prompt injection attempt detected.");
      return;
    }

    if (detectUnsafeHealthcareQuery(cleanedInput)) {
      handleResponse("error", "This assistant cannot provide unsafe medical guidance.");
      return;
    }

    sendMessage(cleanedInput);
  };

  const handleResponse = (status: ChatStatus, message: string) => {
    setStatus(status);
    if (status === 'error') {
      setInputError(message);
      setStatus("ready");
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6 relative size-full h-[calc(100vh-4rem)]">
      <div className="flex flex-col h-full">
        <Conversation className="h-full">
          <ConversationContent>
            {messages.map((message) => (
              <div key={message.id}>
                {message.parts.map((part, i) => {
                  switch (part.type) {
                    case "text":
                      return (
                        <Fragment key={`${message.id}-${i}`}>
                          <Message from={message.role}>
                            <MessageContent>
                              <Response>{part.text}</Response>
                              {/* Sources */}
                              {typeof message.sources !== 'undefined' && message.sources?.length > 0 && (
                                <div className="mt-4">
                                  <p className="text-xs text-gray-500">
                                    Retrieved {message.sources.length} relevant chunks
                                  </p>
                                  <div className="space-y-3">
                                    {message.sources.map((source, idx) => (
                                      <details
                                        key={idx}
                                        className="p-1"
                                      >
                                        <summary className="cursor-pointer text-sm font-medium">
                                          📄 {source.filename}
                                          {" "}— Page {source.page}
                                        </summary>

                                        <div className="mt-3 space-y-2">
                                          {/* Similarity Score */}
                                          {source.score && (
                                            <p className="text-xs text-gray-500">
                                              Similarity Score:
                                              {" "}
                                              {source.score.toFixed(2)}
                                            </p>
                                          )}

                                          {/* Chunk Preview */}
                                          <p className="text-sm text-gray-700 whitespace-pre-wrap">
                                            {source.preview}
                                          </p>
                                        </div>
                                      </details>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </MessageContent>
                          </Message>
                        </Fragment>
                      );
                    default:
                      return null;
                  }
                })}
              </div>
            ))}
            {(status === "submitted" || status === "streaming") && <Loader />}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>

        <PromptInput onSubmit={handleSubmit} className="mt-4">
          <PromptInputBody>
            <PromptInputTextarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </PromptInputBody>
          <PromptInputToolbar>
            <PromptInputTools>
              {/* Model selector, web search, etc. */}
            </PromptInputTools>
            <PromptInputSubmit disabled={!input && !status} status={status} />
          </PromptInputToolbar>
        </PromptInput>
        <div className="text-xs text-gray-500 p-3 mb-3">
          This assistant provides informational support only and is not a substitute for professional medical advice.
          {inputError && (
            <div className="text-xs text-red-500 mt-2">
              {inputError}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
