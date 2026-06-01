from sentence_transformers import SentenceTransformer
model = None

def load_model():
    global model
    if model is None:
        model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    return model

def embed(sentences):
    m = load_model()
    return m.encode(sentences, batch_size=32, show_progress_bar=True)

def embed_query(query):
    m = load_model()
    return m.encode(f"Represent this sentence for searching relevant passages: +{query}")