from embeddings.embedder import load_model


def dense_search (collection, query, n = 8):

    model = load_model()
    embedded_query = model.encode(f"Represent this sentence for searching relevant passages: +{query}")

    results = collection.query(
            query_embeddings = embedded_query,
            n_results = n
    )
    chunks = []
    for i in range (len(results["documents"][0])):
        chunks.append(
            {
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "id": results["ids"][0][i], 
            "score": 1 - results["distances"][0][i]
            }
        )
    return chunks
