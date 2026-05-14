def rerank_results(query, results):

    # SORT BY BEST RELEVANCE
    reranked = sorted(
        results,
        key=lambda x: x["score"]
    )

    return reranked[:5]