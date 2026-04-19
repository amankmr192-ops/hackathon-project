from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection(name="jobs")

def store_job(jd_text):
    embedding = model.encode(jd_text).tolist()
    collection.add(documents=[jd_text], embeddings=[embedding], ids=["job1"])

def match_resume(resume_text):
    query_embedding = model.encode(resume_text).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    return results