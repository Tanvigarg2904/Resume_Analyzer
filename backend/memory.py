import os
import numpy as np
from supabase import create_client
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

class MemoryStore:

    def __init__(self):
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text):
        return self.model.encode(text).tolist()

    def add_resume(self, text):
        emb = self.embed(text)
        self.supabase.table("documents").insert({
            "content": text,
            "embedding": emb
        }).execute()

    def add_job(self, title, desc):
        emb = self.embed(desc)
        self.supabase.table("jobs").insert({
            "title": title,
            "description": desc,
            "embedding": emb
        }).execute()

    def get_resume(self):
        res = self.supabase.table("documents").select("embedding").limit(1).execute()
        return res.data[0]["embedding"]

    def match_jobs(self, resume_vec, top_k=5):

        rows = self.supabase.table("jobs").select("*").execute().data

        scored = []

        for r in rows:
            if not r.get("embedding"):
                continue

            jvec = np.array(r["embedding"])
            score = float(cosine_similarity([resume_vec], [jvec])[0][0])

            scored.append({
                "title": r.get("title", "Job Role"),
                "description": r.get("description", ""),
                "score": int(score * 100)
            })

        return sorted(scored, key=lambda x: -x["score"])[:top_k]
