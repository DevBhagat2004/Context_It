import  os
from pypdf import PdfReader
from ingest.chunker import sendData
from embeddings.embedder import embed
from storage.vectordb import storeData
from storage.vectordb import init
from storage.vectordb import collection_to_chunks
from retrieval.dense import dense_search
from retrieval.sparse import BM25
from retrieval.fusion import fuse
from generation.llm import generate

def menu():
    print("1. PDF")
    print("2. Requery")
    print("3. Just Query")
    print("X Exit")

def getPath():
    name = input("File Name --> ")
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir,"documents",f"{name}")
    return file_path
    

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

def dbFlow(all_data):
    all_data.extend(load_pdf(getPath()))
    all_chunks,sentences = sendData(all_data)
    embeddings = embed(sentences)
    collection  = storeData(all_chunks, embeddings)
    return all_chunks, collection

def searchFlow(all_chunks, collection, query, size):
    sparse = BM25(all_chunks, query, size)
    dense = dense_search(collection, query, size)
    return fuse(dense, sparse)

if __name__ == "__main__":
    print("Hello Please selected which file you want to process")
    menu()
    option = input ("Your choice --> ")
    all_data = []
    all_chunks = []
    collection = None
    while option.lower() != 'x':
        print()
        # Load data & query phase
        if (option == '1'):
            all_chunks,collection  = dbFlow(all_data)
            #Query phase
            query = input ("What your query? --> ")
            #Find the best chunks
            best_chunks = searchFlow(all_chunks, collection, query, 5)
            #generate the out put
            generate(query,best_chunks)
        # Re-query case
        elif (option == '2'):
            
            if not all_chunks or not collection:
                print("Please load a document first")
            else:
                query = input ("What your query? --> ")
                #Find the best chunks
                best_chunks = searchFlow(all_chunks, collection, query, 5)
                #Generating result
                generate(query,best_chunks)
        elif (option == '3'):
            existing_collection = init()
            existing_all_chunks = collection_to_chunks()
            query = input ("What your query? --> ")
            #Find the best chunks
            best_chunks = searchFlow(existing_all_chunks,existing_collection, query, 5)
            #Generating result
            generate(query,best_chunks)
        # Invalid input
        else:
            print("Error, unknown command, try again...")
        print()       
        menu()
        option = input ("Your choice --> ")
    print()