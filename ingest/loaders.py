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
    while option.lower() != 'x':
        print()
        # Load data & query phase
        if (option == '1'):
            all_data.extend(load_pdf(getPath()))
            # Transforming the pdf
            all_chunks,sentences = sendData(all_data)
            # Embedding text
            embeddings = embed(sentences)
            # Making the vectordb
            collection  = storeData(all_chunks, embeddings)
            #Query phase
            query = input ("What your query?")
            #Doing sparse & dense search
            sparse = BM25(all_chunks, query, 5)
            dense = dense_search(collection, query, 5)
            # Fusing results of dense & sparse
            chunks = fuse(dense, sparse)
            #generate the out put
            generate(query,chunks)
            print()
            menu()
        # Re-query case
        elif (option == '2'):
            try:
                if not all_chunks or not collection:
                    print("One of them is empty or falsy")
                    print("Please load a document first")
                    print()
                    menu()
            except NameError:
                print("One of the variables is undefined")
                print("Please load a document first")
                print()
                menu()
            else:
                query = input ("What your query?")
                # Doing sparse & dense search
                sparse = BM25(all_chunks, query, 5)
                dense = dense_search(collection, query, 5)
                # Fusing results of dense & sparse
                chunks = fuse(dense, sparse)
                #Generating result
                generate(query,chunks)
                print()
                menu()
        # Invalid input
        else:
            print("Error, unknown command, try again...")
        print()       
        menu()
        option = input ("Your choice --> ")
    print()




