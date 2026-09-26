from dataclasses import dataclass


@dataclass(frozen=True)
class RiskAssessment:
    score: float
    reasons: tuple[str, ...]


def assess_uncertainty(answer: str, context_count: int) -> RiskAssessment:
    text = answer.lower()
    score = 0.0
    reasons: list[str] = []

    if context_count == 0:
        score += 0.6
        reasons.append("no_validated_context")
    if any(term in text for term in ("maybe", "probably", "not sure", "uncertain")):
        score += 0.25
        reasons.append("uncertainty_language")
    if len(answer.strip()) < 20:
        score += 0.2
        reasons.append("very_short_answer")

    return RiskAssessment(min(score, 1.0), tuple(reasons))
