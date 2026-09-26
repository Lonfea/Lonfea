from pydantic import BaseModel, Field


class BenchmarkCase(BaseModel):
    id: str
    question: str
    evidence: list[str]
    reference_answer: str
    required_terms: list[str] = Field(default_factory=list)
    expected_citations: list[int] = Field(default_factory=list)
    abstain: bool = False


class Prediction(BaseModel):
    id: str
    answer: str
    citations: list[int] = Field(default_factory=list)
