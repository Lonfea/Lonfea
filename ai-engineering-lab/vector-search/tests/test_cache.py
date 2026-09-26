from app.cache import EmbeddingCache


def test_embedding_cache_roundtrip(tmp_path):
    cache = EmbeddingCache(str(tmp_path / "cache.db"))
    key = cache.key("hello", "dense", "sparse")
    assert cache.get(key) is None

    cache.put(key, [0.1, 0.2], [1, 7], [0.5, 0.8])
    dense, indices, values = cache.get(key)

    assert dense == [0.1, 0.2]
    assert indices == [1, 7]
    assert values == [0.5, 0.8]
