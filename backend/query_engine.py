import re
import numpy as np
from sqlalchemy import text

class QueryEngine:
    def __init__(self, schema: dict, engine, doc_processor):
        self.schema = schema
        self.engine = engine
        self.docs = doc_processor

    def process_query(self, user_query: str) -> dict:
        q = user_query.lower()

        # Document search trigger words (tweak as needed)
        doc_triggers = ["resume", "cv", "python", "skill", "experience", "resume", "skills"]
        if any(tok in q for tok in doc_triggers):
            return self._doc_search(user_query)

        # Aggregation: average salary by department
        if "average" in q or "avg" in q:
            sql = "SELECT department, AVG(salary) as average_salary FROM employees GROUP BY department"
            with self.engine.connect() as conn:
                rows = conn.execute(text(sql)).mappings().all()
            return {"type": "sql", "sql": sql, "results": [dict(r) for r in rows]}

        # Count / how many
        if "how many" in q or "count" in q or "number of" in q:
            sql = "SELECT COUNT(*) as count FROM employees"
            with self.engine.connect() as conn:
                rows = conn.execute(text(sql)).mappings().all()
            return {"type": "sql", "sql": sql, "results": [dict(r) for r in rows]}

        # Filter by department pattern: "in engineering"
        m = re.search(r"in (\w+)", q)
        table = next(iter(self.schema.keys())) if self.schema else "employees"
        if m:
            dept = m.group(1).capitalize()
            sql = f"SELECT * FROM {table} WHERE department = :dept LIMIT 100"
            with self.engine.connect() as conn:
                rows = conn.execute(text(sql), {"dept": dept}).mappings().all()
            return {"type": "sql", "sql": sql, "results": [dict(r) for r in rows]}

        # Default: return first 100 rows
        sql = f"SELECT * FROM {table} LIMIT 100"
        with self.engine.connect() as conn:
            rows = conn.execute(text(sql)).mappings().all()
        return {"type": "sql", "sql": sql, "results": [dict(r) for r in rows]}

    def _doc_search(self, query: str) -> dict:
        # If using model embeddings:
        if hasattr(self.docs, "model"):
            q_emb = self.docs.model.encode(query)
            sims = []
            for d in self.docs.docs:
                emb = d["embedding"]
                # cosine similarity
                sim = float(np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb) + 1e-9))
                sims.append(sim)
            best = int(np.argmax(sims))
            return {"type": "docs", "score": sims[best], "result": self.docs.docs[best]["text"]}
        # Fallback substring search (no embeddings)
        for d in self.docs.docs[::-1]:
            if query.lower() in d["text"].lower():
                return {"type": "docs", "result": d["text"]}
        return {"type": "docs", "result": None}
