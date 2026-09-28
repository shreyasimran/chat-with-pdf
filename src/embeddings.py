from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLm-L6-v2")
def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings