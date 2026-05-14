import { ChatMessage } from "@/types/chat";
import { NextResponse } from "next/server";
import { apiFetch } from "@/lib/api";

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const cleanedMessages = messages.filter(
      (message: ChatMessage) => {

        const text =
          message.parts?.[0]?.text?.trim();

        return text;
      }
    );

    const latestMessage =
      cleanedMessages[cleanedMessages.length - 1]
        ?.parts?.[0]?.text || "";

    const response = await apiFetch("chat", {
      method: "POST",
      body: JSON.stringify({
        question: latestMessage,
        messages: cleanedMessages.slice(-6),
      }),
      headers: { "Content-Type": "application/json" }
    })

    const data = await response?.json();
    return NextResponse.json({
      messages: [
        {
          id: crypto.randomUUID(),
          role: "assistant",
          parts: [
            {
              type: "text",
              text: data.answer
            }
          ],
          sources: data.sources
        }
      ]
    });
  } catch (error) {
    console.error("Error streaming chat completion:", error);
    return new Response("Failed to stream chat completion", { status: 500 });
  }
}
