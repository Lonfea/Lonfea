import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class EvalSummary:
    domain_accuracy: float
    general_accuracy: float
    general_drop: float


def compare(before: dict, after: dict, max_general_drop: float = 0.03) -> EvalSummary:
    domain_before = float(before["domain_accuracy"])
    domain_after = float(after["domain_accuracy"])
    general_before = float(before["general_accuracy"])
    general_after = float(after["general_accuracy"])

    if domain_after < domain_before:
        raise RuntimeError(
            f"Domain score regressed: {domain_after:.3f} < {domain_before:.3f}"
        )

    drop = general_before - general_after
    if drop > max_general_drop:
        raise RuntimeError(
            f"Potential catastrophic forgetting: general score dropped by {drop:.3f}"
        )

    return EvalSummary(
        domain_accuracy=domain_after,
        general_accuracy=general_after,
        general_drop=drop,
    )


def main() -> None:
    before = json.loads(Path("reports/before.json").read_text(encoding="utf-8"))
    after = json.loads(Path("reports/after.json").read_text(encoding="utf-8"))
    summary = compare(before, after)
    print(json.dumps(asdict(summary), indent=2))


if __name__ == "__main__":
    main()
