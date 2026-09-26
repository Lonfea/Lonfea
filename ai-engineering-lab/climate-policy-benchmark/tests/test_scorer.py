from benchmark.schema import BenchmarkCase, Prediction
from benchmark.scorer import score_case


def test_supported_answer_passes():
    case = BenchmarkCase(
        id="x",
        question="Target?",
        evidence=["[1] Target is 55% by 2030."],
        reference_answer="The target is 55% by 2030.",
        required_terms=["55%", "2030"],
        expected_citations=[1],
    )
    prediction = Prediction(id="x", answer="The target is 55% by 2030.", citations=[1])
    assert score_case(case, prediction)["passed"]


def test_missing_citation_fails():
    case = BenchmarkCase(
        id="x",
        question="Target?",
        evidence=["[1] Target is 55% by 2030."],
        reference_answer="The target is 55% by 2030.",
        required_terms=["55%"],
        expected_citations=[1],
    )
    prediction = Prediction(id="x", answer="The target is 55% by 2030.", citations=[])
    assert not score_case(case, prediction)["passed"]
