#import  bs4, os, pathlib
from pypdf import PdfReader
from ingest.chunker import sendData
from embeddings.embedder import embed
from storage.vectordb import storeData
from retrieval.dense import dense_search
from retrieval.sparse import BM25
from retrieval.fusion import fuse
from generation.llm import generate

def menu():
    print("1. PDF")
    print("2. MarkDown")
    print("3. TXT")
    print("X Exit")

def getPath():
    return input("Filepath --> ")
    

def load_pdf(Path):
    data = []
    reader = PdfReader(Path)
    for i in range(len(reader.pages)):
        text = reader.pages[i].extract_text()
        if text.strip():
            data.append({
                "text" : text,
                "metadata": {"source":Path,"page":i+1}
            })
       
    return data



def load_Other(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        data.append({
            "text": f.read(),
            "metadata": {"source":path,"page":1}
        })
    
    return data



if __name__ == "__main__":
    print("Hello Please selected which file you want to process")
    menu()
    option = input ("Your choice --> ")
    all_data = []
    while option != 'x':
        print()
        if (option == '1'):
            all_data.extend(load_pdf(getPath()))
        elif (option == '2'):
            all_data.extend(load_Other(getPath()))
        elif (option == '3'):
            all_data.extend(load_Other(getPath()))
        else:
            print("Error, unknown command, try again...")
        print()       
        menu()
        option = input ("Your choice --> ")
    print()
    all_chunks,sentences = sendData(all_data)
    embeddings = embed(sentences)
    collection  = storeData(all_chunks, embeddings)
    query = input ("What your query?")
    sparse = BM25(all_chunks, query, 5)
    print("------------------------------------------------------------------")
    dense = dense_search(collection, query, 5)

    chunks = fuse(dense, sparse)

    generate(query,chunks)




