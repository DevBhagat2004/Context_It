from embeddings.embedder import embed_query
from rank_bm25 import BM25Okapi

def build_index(all_chunks):
    tokenized_chunks = [chunk["text"].lower().split() for chunk in all_chunks]
    index = BM25Okapi(tokenized_chunks)
    return index

def BM25(all_chunks, query,n = 8):
    tokenized_query = query.lower().split()
    index = build_index (all_chunks)
    scores = index.get_scores(tokenized_query)

    scored_chunks = sorted(
        zip(scores,all_chunks),
        key = lambda x: x[0],
        reverse = True
    )

    result = []
    for score, chunk in scored_chunks[:n]:
        result.append(
            {
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "id": f"{chunk['metadata']['source'].replace(' ', '_')}_p{chunk['metadata']['page']}_c{chunk['metadata']['chunk_index']}",
            "score": score
            }
        )

    return result







