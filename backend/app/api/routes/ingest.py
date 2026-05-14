import os
import tempfile

from fastapi import APIRouter, UploadFile, File, Depends

from app.services.ingestion.pdf_loader import load_pdf
from app.services.ingestion.chunk_service import split_documents
from app.services.ingestion.embedding_service import get_embeddings
from app.services.ingestion.vector_store import get_vector_store
from app.services.ingestion.document_store import save_document_chunk

from app.auth.rbac import require_permissions
from app.auth.permissions import Permission

router = APIRouter()

# 
@router.post("/ingest")
async def ingest_pdf(
    file: UploadFile = File(...),
    user = Depends(require_permissions([Permission.INGEST]))
):

    # Validate PDF
    if file.content_type != "application/pdf":
        return {
            "error": "Only PDF files are allowed"
        }
    
    if file.size > 10 * 1024 * 1024:
        return {
            "error": "File size should be lower than 10MB"
        }

    # Save temp file
    temp_dir = tempfile.gettempdir()

    file_path = os.path.join(
        temp_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Load PDF
    documents = load_pdf(file_path)

    # Chunk documents
    chunks = split_documents(documents)

    print(
        f"Total chunks: {len(chunks)}"
    )

    for chunk in chunks:

        print(
            "Processing chunk..."
        )

        chunk.metadata["filename"] = file.filename

        chunk.metadata["upload_type"] = "pdf"

        chunk.metadata["document_category"] = "healthcare"

        chunk.metadata["source"] = file.filename

        save_document_chunk(
            content=chunk.page_content,
            metadata=chunk.metadata
        )

    return {
        "message": f"Saved {len(chunks)} ingested successfully",
        "chunks": len(chunks)
    }