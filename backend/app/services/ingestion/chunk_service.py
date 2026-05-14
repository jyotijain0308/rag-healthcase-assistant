from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=75,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(
        documents
    )

    print(f"\nTOTAL CHUNKS: {len(chunks)}")

    return chunks