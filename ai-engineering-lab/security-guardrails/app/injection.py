import re
from dataclasses import dataclass


@dataclass(frozen=True)
class InjectionFinding:
    rule: str
    matched: str


_PATTERNS = {
    "instruction_override": re.compile(
        r"\b(ignore|disregard|forget)\b.{0,40}\b(previous|above|system|developer)\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "secret_exfiltration": re.compile(
        r"\b(reveal|show|print|leak|dump)\b.{0,50}\b(prompt|secret|api key|token)\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "role_hijack": re.compile(
        r"\b(you are now|act as|pretend to be)\b.{0,50}\b(system|developer|administrator)\b",
        re.IGNORECASE | re.DOTALL,
    ),
}


def detect_prompt_injection(text: str) -> list[InjectionFinding]:
    findings = []
    for name, pattern in _PATTERNS.items():
        match = pattern.search(text)
        if match:
            findings.append(InjectionFinding(name, match.group(0)))
    return findings
