from rank_bm25 import BM25Okapi

from app.services.ingestion.vector_store import (
    get_vector_store
)

from app.services.ingestion.document_store import (
    get_all_document_chunks
)

SEMANTIC_K = 10

MMR_K = 6

FETCH_K = 20

SIMILARITY_THRESHOLD = 0.4

def hybrid_search(query: str):

    vector_store = get_vector_store()
    # embeddings = get_embeddings()

    # vector_store = Chroma(
    #     persist_directory=CHROMA_PATH,
    #     embedding_function=embeddings
    # )

    print("\n======================")
    print("SEMANTIC SEARCH")

    # STEP 1 — SEMANTIC SEARCH
    semantic_results = (
        vector_store.similarity_search_with_score(
            query=query,
            k=SEMANTIC_K
        )
    )

    filtered_semantic = []

    for doc, score in semantic_results:

        print("\nFILE:")
        print(doc.metadata.get("filename"))

        print("SCORE:")
        print(score)

        # FILTER WEAK RESULTS
        if score > SIMILARITY_THRESHOLD:
            continue

        filtered_semantic.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": float(score),
            "relevance_score": round(
                1 - score,
                4
            ),
            "source": "semantic"
        })

    print("\n======================")
    print("BM25 SEARCH")

    # STEP 2 — BM25 SEARCH
    # collection = vector_store.get()

    # documents = collection["documents"]

    # metadatas = collection["metadatas"]

    stored_documents = get_all_document_chunks()

    documents = [
        item["content"]
        for item in stored_documents
    ]

    metadatas = [
        item["metadata"]
        for item in stored_documents
    ]

    # SAFETY CHECK
    if not documents:
        print("No documents found for BM25")
        return filtered_semantic

    tokenized_docs = [
        doc.split(" ")
        for doc in documents
    ]

    bm25 = BM25Okapi(tokenized_docs)

    keyword_scores = bm25.get_scores(
        query.split(" ")
    )

    keyword_results = sorted(
        zip(
            documents,
            metadatas,
            keyword_scores
        ),
        key=lambda x: x[2],
        reverse=True
    )[:5]

    formatted_keyword_results = []

    BM25_THRESHOLD = 0.1

    for doc, metadata, score in keyword_results:

        print("\nBM25 SCORE:")
        print(score)

        # SKIP LOW/IRRELEVANT RESULTS
        if score <= BM25_THRESHOLD:
            continue

        formatted_keyword_results.append({
            "content": doc,
            "metadata": metadata,
            "score": float(score),
            "relevance_score": round(
                float(score),
                4
            ),
            "source": "bm25"
        })

    print("\n======================")
    print("MMR SEARCH")

    # STEP 3 — MMR DIVERSIFICATION
    mmr_docs = (
        vector_store.max_marginal_relevance_search(
            query=query,
            k=MMR_K,
            fetch_k=FETCH_K,
            lambda_mult=0.7
        )
    )

    mmr_contents = set()

    for doc in mmr_docs:

        mmr_contents.add(
            doc.page_content
        )

    print("\n======================")
    print("COMBINING RESULTS")

    final_results = []

    seen = set()

    # STEP 4 — ADD SEMANTIC RESULTS
    for result in filtered_semantic:

        content = result["content"]

        # KEEP ONLY MMR DIVERSIFIED RESULTS
        if content not in mmr_contents:
            continue

        # REMOVE DUPLICATES
        if content in seen:
            continue

        seen.add(content)

        final_results.append(result)

    # STEP 5 — ADD BM25 RESULTS
    for result in formatted_keyword_results:

        content = result["content"]

        if content in seen:
            continue

        seen.add(content)

        final_results.append(result)

    print("\n======================")
    print("FINAL RETRIEVAL RESULTS")

    for index, result in enumerate(
        final_results
    ):

        print("\n----------------------")
        print(f"RESULT {index + 1}")

        print("SOURCE:")
        print(result["source"])

        print("SCORE:")
        print(result["score"])

        print("FILE:")
        print(
            result["metadata"].get(
                "filename"
            )
        )

        print("PAGE:")
        print(
            result["metadata"].get(
                "page"
            )
        )

    return final_results