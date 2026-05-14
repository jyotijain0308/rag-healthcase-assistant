from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3",
    temperature=0
)

def build_chat_history(messages):

    history = []

    for message in messages:

        text = ""

        if message.parts:

            text = (
                message.parts[0].text
            )

        history.append(
            f"{message.role}: {text}"
        )

    return "\n".join(history)

def generate_response(context, question, chat_history):

    prompt = f"""
You are a healthcare knowledge assistant.

STRICT RULES:

- Answer ONLY from provided context
- Never invent medical information
- Never hallucinate
- If answer is unavailable say:
  "I could not find relevant information."
- Cite retrieved sources
- Be medically cautious
- Never provide unsafe medical advice"

Conversation History:
{chat_history}

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content