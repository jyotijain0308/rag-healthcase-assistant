import json

from sqlalchemy import text

from app.db.db_session import (
    SessionLocal
)

def save_document_chunk(
    content: str,
    metadata: dict
):

    db = SessionLocal()

    try:

        print("\nSaving document chunk...")
        print("CONTENT:", content[:100])

        query = text("""
            INSERT INTO document_chunks
            (
                content,
                document_metadata
            )
            VALUES
            (
                :content,
                :document_metadata
            )
        """)

        db.execute(
            query,
            {
                "content": content,
                "document_metadata": json.dumps(
                    metadata
                )
            }
        )

        db.commit()

        print("Chunk saved successfully")

    except Exception as e:

        print(
            "ERROR SAVING CHUNK:",
            str(e)
        )

        db.rollback()

    finally:

        db.close()


def get_all_document_chunks():

    db = SessionLocal()

    try:

        query = text("""
            SELECT
                id,
                content,
                document_metadata
            FROM document_chunks
        """)

        result = db.execute(query)

        rows = result.fetchall()

        documents = []

        for row in rows:

            documents.append({
                "id": row[0],
                "content": row[1],
                "metadata": row[2]
            })

        print(
            f"Fetched {len(documents)} chunks"
        )

        return documents

    except Exception as e:

        print(
            "ERROR FETCHING CHUNKS:",
            str(e)
        )

        return []

    finally:

        db.close()