import json
import sys
from pathlib import Path


def check(report_path: str) -> list[str]:
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    aggregate = report["aggregate"]
    failures = []

    thresholds = {
        "pass_rate": 0.90,
        "mean_faithfulness": 0.85,
        "mean_answer_relevancy": 0.80,
        "citation_accuracy": 0.95,
    }
    for metric, minimum in thresholds.items():
        value = float(aggregate[metric])
        if value < minimum:
            failures.append(f"{metric}: {value:.3f} < {minimum:.3f}")
    return failures


if __name__ == "__main__":
    failures = check(sys.argv[1])
    if failures:
        raise SystemExit("AI quality gate failed:\n- " + "\n- ".join(failures))
