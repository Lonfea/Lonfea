import uuid

from fastembed import SparseTextEmbedding, TextEmbedding
from qdrant_client import QdrantClient, models

from app.cache import EmbeddingCache


class HybridStore:
    def __init__(
        self,
        url: str = "http://localhost:6333",
        collection: str = "documents",
        cache_path: str = "embedding_cache.db",
    ):
        self.client = QdrantClient(url=url)
        self.collection = collection
        self.dense_model_name = "BAAI/bge-small-en-v1.5"
        self.sparse_model_name = "Qdrant/bm25"
        self.dense_model = TextEmbedding(self.dense_model_name)
        self.sparse_model = SparseTextEmbedding(self.sparse_model_name)
        self.cache = EmbeddingCache(cache_path)

    def ensure_collection(self) -> None:
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config={
                    "dense": models.VectorParams(
                        size=384,
                        distance=models.Distance.COSINE,
                    )
                },
                sparse_vectors_config={
                    "sparse": models.SparseVectorParams()
                },
                hnsw_config=models.HnswConfigDiff(
                    m=16,
                    ef_construct=128,
                ),
                optimizers_config=models.OptimizersConfigDiff(
                    indexing_threshold=20_000
                ),
            )
            self.client.create_payload_index(
                self.collection,
                field_name="tenant_id",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )
            self.client.create_payload_index(
                self.collection,
                field_name="source",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )

    def _embed(self, text: str):
        key = self.cache.key(text, self.dense_model_name, self.sparse_model_name)
        cached = self.cache.get(key)
        if cached:
            return cached

        dense = list(next(self.dense_model.embed([text])))
        sparse = next(self.sparse_model.embed([text]))
        indices = sparse.indices.tolist()
        values = sparse.values.tolist()
        dense_list = [float(value) for value in dense]
        values_list = [float(value) for value in values]
        self.cache.put(key, dense_list, indices, values_list)
        return dense_list, indices, values_list

    def upsert(self, text: str, *, tenant_id: str, source: str) -> str:
        dense, indices, values = self._embed(text)
        point_id = str(uuid.uuid4())
        self.client.upsert(
            self.collection,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector={
                        "dense": dense,
                        "sparse": models.SparseVector(
                            indices=indices,
                            values=values,
                        ),
                    },
                    payload={
                        "text": text,
                        "tenant_id": tenant_id,
                        "source": source,
                    },
                )
            ],
        )
        return point_id

    def search(self, query: str, *, tenant_id: str, limit: int = 10):
        dense, indices, values = self._embed(query)
        tenant_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="tenant_id",
                    match=models.MatchValue(value=tenant_id),
                )
            ]
        )
        return self.client.query_points(
            collection_name=self.collection,
            prefetch=[
                models.Prefetch(
                    query=dense,
                    using="dense",
                    filter=tenant_filter,
                    limit=max(20, limit * 2),
                ),
                models.Prefetch(
                    query=models.SparseVector(indices=indices, values=values),
                    using="sparse",
                    filter=tenant_filter,
                    limit=max(20, limit * 2),
                ),
            ],
            query=models.RrfQuery(rrf=models.Rrf(k=60)),
            limit=limit,
            with_payload=True,
        ).points

    def snapshot(self):
        return self.client.create_snapshot(collection_name=self.collection)
