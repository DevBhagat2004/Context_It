import chromadb

def init():
    client = chromadb.PersistentClient(path="./db")
    collection = client.get_or_create_collection(name="documents")
    return collection

def collection_to_chunks():
    collection = init().get()
    all_chunks = []
    for i in range(len(collection["ids"])):
        all_chunks.append({
                "text" : collection["documents"][i],
                "metadata": collection["metadatas"][i]
            })
    return all_chunks


def addData(all_chunks, embeddings, collection):
    documents = []
    ids = []
    metadatas= []
    
    for chunk in all_chunks:
        #Making the Ids
        source = chunk["metadata"]["source"].replace(" ", "_")
        page   = chunk["metadata"]["page"]
        index  = chunk["metadata"]["chunk_index"]
        ids.append(f"{source}_p{page}_c{index}")
        # Making the documents
        documents.append(chunk["text"])
        metadatas.append(chunk["metadata"])


    collection.add(
        ids = ids,
        documents = documents,
        embeddings = embeddings,
        metadatas = metadatas
    )    

    return collection

def storeData(all_chunks, embeddings):
    collection = init()
    return addData(all_chunks, embeddings, collection)
