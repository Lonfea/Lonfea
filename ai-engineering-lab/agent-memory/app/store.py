import json
import time
import uuid

from fastembed import TextEmbedding
from qdrant_client import QdrantClient, models
from redis import Redis

from app.policy import MemoryPolicy, compress_messages


class AgentMemory:
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        qdrant_url: str = "http://localhost:6333",
        collection: str = "agent_memory",
        policy: MemoryPolicy | None = None,
    ):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.qdrant = QdrantClient(url=qdrant_url)
        self.collection = collection
        self.policy = policy or MemoryPolicy()
        self.embedder = TextEmbedding("BAAI/bge-small-en-v1.5")

    def ensure_collection(self):
        if not self.qdrant.collection_exists(self.collection):
            self.qdrant.create_collection(
                self.collection,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE,
                ),
            )
            self.qdrant.create_payload_index(
                self.collection,
                field_name="user_id",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

    @staticmethod
    def _session_key(user_id: str, session_id: str) -> str:
        return f"memory:session:{user_id}:{session_id}"

    def append_turn(self, user_id: str, session_id: str, role: str, content: str):
        clean = content[: self.policy.max_message_chars]
        payload = json.dumps(
            {
                "role": role,
                "content": clean,
                "ts": time.time(),
            }
        )
        key = self._session_key(user_id, session_id)
        with self.redis.pipeline() as pipe:
            pipe.rpush(key, payload)
            pipe.ltrim(key, -self.policy.short_term_turns, -1)
            pipe.expire(key, 60 * 60 * 24 * 7)
            pipe.execute()

    def short_term(self, user_id: str, session_id: str) -> list[dict]:
        key = self._session_key(user_id, session_id)
        return [json.loads(item) for item in self.redis.lrange(key, 0, -1)]

    def compressed_context(self, user_id: str, session_id: str) -> str:
        messages = [
            f"{row['role']}: {row['content']}"
            for row in self.short_term(user_id, session_id)
        ]
        return compress_messages(messages)

    def remember(self, user_id: str, content: str, *, kind: str = "fact") -> str:
        self.ensure_collection()
        vector = list(next(self.embedder.embed([content])))
        point_id = str(uuid.uuid4())
        self.qdrant.upsert(
            self.collection,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=[float(value) for value in vector],
                    payload={
                        "user_id": user_id,
                        "content": content,
                        "kind": kind,
                        "created_at": time.time(),
                    },
                )
            ],
        )
        return point_id

    def recall(self, user_id: str, query: str) -> list[dict]:
        self.ensure_collection()
        vector = list(next(self.embedder.embed([query])))
        points = self.qdrant.query_points(
            self.collection,
            query=[float(value) for value in vector],
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=user_id),
                    )
                ]
            ),
            limit=self.policy.long_term_limit,
            score_threshold=self.policy.min_long_term_score,
            with_payload=True,
        ).points
        return [
            {
                "id": str(point.id),
                "score": float(point.score),
                "content": point.payload.get("content"),
                "kind": point.payload.get("kind"),
            }
            for point in points
        ]

    def forget(self, user_id: str, memory_ids: list[str]) -> None:
        self.qdrant.delete(
            self.collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="user_id",
                            match=models.MatchValue(value=user_id),
                        ),
                        models.HasIdCondition(has_id=memory_ids),
                    ]
                )
            ),
        )
