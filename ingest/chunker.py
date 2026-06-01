def chunk_text(text, size, overlap):
    start = 0
    chunks = []
    while start < len(text):
        end = size + start
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

def processData(data):
    all_chunks = []
    sentences = []
    for page in data:
        text = page["text"]
        meta= page["metadata"]
        chunks = chunk_text(text,500,50)
        for i, chunk in enumerate (chunks):
            sentences.append(chunk)
            all_chunks.append({
                "text" : chunk,
                "metadata": {"source":meta["source"],
                             "page":  meta["page"],
                             "chunk_index": i}
            })
    return all_chunks, sentences

def sendData(data):
    return  processData(data)


