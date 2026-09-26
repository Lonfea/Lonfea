import re

from benchmark.schema import BenchmarkCase, Prediction


def normalize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def score_case(case: BenchmarkCase, prediction: Prediction) -> dict:
    answer_terms = normalize(prediction.answer)
    reference_terms = normalize(case.reference_answer)

    overlap = len(answer_terms & reference_terms) / max(len(reference_terms), 1)
    required = all(term.lower() in prediction.answer.lower() for term in case.required_terms)
    citation_ok = set(case.expected_citations).issubset(set(prediction.citations))

    if case.abstain:
        abstention_ok = any(
            phrase in prediction.answer.lower()
            for phrase in ("insufficient evidence", "not provided", "cannot determine")
        )
    else:
        abstention_ok = True

    passed = overlap >= 0.50 and required and citation_ok and abstention_ok
    return {
        "id": case.id,
        "lexical_support": overlap,
        "required_terms": required,
        "citation_ok": citation_ok,
        "abstention_ok": abstention_ok,
        "passed": passed,
    }
