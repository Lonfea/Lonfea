import json
import sys
from pathlib import Path

from benchmark.schema import BenchmarkCase, Prediction
from benchmark.scorer import score_case


def load_jsonl(path: str, model):
    return [
        model.model_validate_json(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main(cases_path: str, predictions_path: str) -> None:
    cases = load_jsonl(cases_path, BenchmarkCase)
    predictions = {row.id: row for row in load_jsonl(predictions_path, Prediction)}

    results = []
    for case in cases:
        if case.id not in predictions:
            results.append({"id": case.id, "passed": False, "reason": "missing_prediction"})
            continue
        results.append(score_case(case, predictions[case.id]))

    pass_rate = sum(bool(row["passed"]) for row in results) / max(len(results), 1)
    print(json.dumps({"cases": len(results), "pass_rate": pass_rate, "results": results}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
