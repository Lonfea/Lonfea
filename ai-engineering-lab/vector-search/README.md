# Vector Database at Scale — Qdrant Hybrid Search

A production-oriented vector-search layer with dense + sparse retrieval, reciprocal-rank fusion, metadata isolation, embedding caching, index configuration, and snapshot-based backup.

## Query path

1. embed query into a dense vector and sparse BM25 representation;
2. read through a local embedding cache to avoid duplicate computation;
3. run both retrieval modes as Qdrant prefetches;
4. enforce a tenant metadata filter on **both** branches;
5. fuse ranks with RRF;
6. return payload-bearing top results.

## Operational design

- HNSW parameters are configured explicitly.
- `tenant_id` and `source` payload indexes support common filters.
- embedding cache keys include model names so model upgrades cannot silently reuse incompatible vectors.
- `snapshot()` uses Qdrant's collection snapshot API for backup/recovery workflows.
- Docker volumes persist both collection data and snapshot files.

## Run

    docker compose up -d
    pip install -e ".[dev]"

Then:

    from app.store import HybridStore

    store = HybridStore()
    store.ensure_collection()
    store.upsert("Climate risk is increasing.", tenant_id="acme", source="report.pdf")
    hits = store.search("climate risk", tenant_id="acme")

## Scaling notes

A real distributed deployment should benchmark shard count, replication, HNSW parameters, payload selectivity, batch upserts, and snapshot/restore procedures against its own corpus and SLOs. This project deliberately avoids claiming a QPS number without a measured benchmark.
