import hashlib
import json
import sqlite3


class EmbeddingCache:
    def __init__(self, path: str = "embedding_cache.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS embeddings (
              cache_key TEXT PRIMARY KEY,
              dense TEXT NOT NULL,
              sparse_indices TEXT NOT NULL,
              sparse_values TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    @staticmethod
    def key(text: str, dense_model: str, sparse_model: str) -> str:
        payload = f"{dense_model}\0{sparse_model}\0{text}".encode()
        return hashlib.sha256(payload).hexdigest()

    def get(self, key: str):
        row = self.conn.execute(
            "SELECT dense, sparse_indices, sparse_values FROM embeddings WHERE cache_key=?",
            (key,),
        ).fetchone()
        if not row:
            return None
        return json.loads(row[0]), json.loads(row[1]), json.loads(row[2])

    def put(self, key: str, dense: list[float], indices: list[int], values: list[float]):
        with self.conn:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO embeddings
                (cache_key, dense, sparse_indices, sparse_values)
                VALUES (?, ?, ?, ?)
                """,
                (key, json.dumps(dense), json.dumps(indices), json.dumps(values)),
            )
