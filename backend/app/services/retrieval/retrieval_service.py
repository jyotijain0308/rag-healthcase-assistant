from app.services.retrieval.hybrid_search import hybrid_search
from app.services.retrieval.reranker import rerank_results

def retrieve_documents(query: str):

    # STEP 1
    results = hybrid_search(query)

    # STEP 2
    reranked_results = rerank_results(
        query,
        results
    )

    return reranked_results