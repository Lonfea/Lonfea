from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryPolicy:
    short_term_turns: int = 12
    max_message_chars: int = 4000
    long_term_limit: int = 8
    min_long_term_score: float = 0.45


def compress_messages(messages: list[str], max_chars: int = 6000) -> str:
    """Deterministic fallback compressor for context budgeting."""
    selected: list[str] = []
    used = 0
    for message in reversed(messages):
        clean = " ".join(message.split())
        remaining = max_chars - used
        if remaining <= 0:
            break
        piece = clean[:remaining]
        selected.append(piece)
        used += len(piece)
    return "\n".join(reversed(selected))
