SIMILARITY_THRESHOLD = 0.4

def filter_results(semantic_results):

    filtered_results = []

    seen = set()

    for doc, score in semantic_results:

        # FILTER LOW RELEVANCE
        if score > SIMILARITY_THRESHOLD:
            continue

        filename = (
            doc.metadata.get("filename")
        )

        page = doc.metadata.get("page")

        key = f"{filename}-{page}"

        # REMOVE DUPLICATES
        if key in seen:
            continue

        seen.add(key)

        filtered_results.append({
            "document": doc,
            "score": float(score),
            "relevance_score":
                round(1 - score, 4)
        })

    return filtered_results