# Climate Policy AI Benchmark

An open benchmark scaffold for evidence-grounded climate-policy question answering.

It is designed around failure modes that matter in policy analysis:
- answering from supplied evidence rather than prior assumptions;
- distinguishing approved text from superseded drafts;
- abstaining when a requested value is absent;
- citing the evidence used;
- preserving important numeric and policy terms.

## Why climate policy?

This benchmark connects AI engineering with climate-change management and creates a domain-specific artifact rather than another generic chatbot benchmark.

## Dataset integrity

The committed sample cases are explicitly **fictional fixtures** for testing the benchmark code. They are not represented as real policy facts.

A public benchmark release should add a versioned dataset built from redistributable or properly cited public policy documents, with licensing and provenance recorded for every source.

## Prediction format

JSONL:

    {"id":"cp-001","answer":"...","citations":[1]}

## Run

    python -m benchmark.run cases/sample.jsonl predictions.jsonl

## Scoring

The deterministic baseline scorer checks:
- lexical support against the reference;
- required domain terms;
- expected citations;
- correct abstention behavior.

A leaderboard release can add model-graded semantic metrics, but deterministic scoring remains useful for reproducibility.

## Community roadmap

- 500+ reviewed public-document questions;
- difficulty and failure-mode tags;
- frozen train/dev/test splits;
- benchmark card and data statement;
- reproducible submission format;
- public leaderboard generated from submitted result files;
- external contributions through pull requests.
