from langchain_postgres import PGVector

from app.db.database import (
    DATABASE_URL
)

from app.services.ingestion.embedding_service import (
    get_embeddings
)

COLLECTION_NAME = (
    "healthcare_documents"
)

def get_vector_store():

    embeddings = get_embeddings()

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )

    return vector_store