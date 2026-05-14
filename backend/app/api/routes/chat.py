from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.roles import UserRole
from app.auth.rbac import require_permissions
from app.auth.permissions import Permission

from app.services.retrieval.retrieval_service import retrieve_documents
from app.services.llm.llm_service import generate_response
from app.services.llm.llm_service import build_chat_history

from app.utils.security import (
    detect_prompt_injection,
    detect_unsafe_healthcare_query,
    is_meaningless_query
)

from app.models.chat import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(
    request: ChatRequest, 
    user=Depends(require_permissions([Permission.CHAT]))
):

    if detect_prompt_injection(request.question):
        return {
            "answer": (
                "Prompt injection attempt detected."
            ),
            "sources": []
        }

    if detect_unsafe_healthcare_query(request.question):
        return {
            "answer": (
                "This assistant cannot provide "
                "unsafe medical guidance."
            ),
            "sources": []
        }

    if is_meaningless_query(request.question):
        return {
            "answer": (
                "Please ask a meaningful "
                "healthcare-related question."
            ),
            "sources": []
        }

    docs = retrieve_documents(request.question)

    if not docs:
        return {
            "answer": (
                "I could not find relevant "
                "information."
            ),
            "sources": []
        }

    context_chunks = []
    sources = []

    for item in docs:

        content = item["content"]

        metadata = item["metadata"]

        context_chunks.append(content)

        sources.append({
            "filename": metadata.get("filename"),

            "page": metadata.get("page"),

            "score": item.get("relevance_score"),

            "source": item.get("source"),

            "preview": content[:200]
        })

    sources = sorted(
        sources,
        key=lambda x: (
            x["filename"] or "",
            x["page"] or 0
        )
    )

    context = "\n\n".join(
        context_chunks
    )

    conversation_history = build_chat_history(request.messages);

    answer = generate_response(
        context,
        request.question,
        conversation_history
    )

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": len(docs)
    }