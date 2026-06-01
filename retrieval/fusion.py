def get_id(chunk):
    return chunk["id"]

def fuse(dense, sparse):
    all_results = {}

    for rank, chunk in enumerate(sparse):
        id = get_id(chunk)
        all_results[id] = chunk
        chunk["rrf"] = 1/(60+1+rank)

    for rank, chunk in enumerate(dense):
        id = get_id(chunk)

        if id not in all_results:
            all_results[id] = chunk
            chunk["rrf"] = 1/(60+1+rank)

        else: 
            all_results[id]["rrf"]+= 1/(60+1+rank)

    sorted(
        all_results.values(),
        key = lambda chunk: chunk["rrf"],
        reverse = True
    )

    return list(all_results.values())[:7]