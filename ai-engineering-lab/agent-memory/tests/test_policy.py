from app.policy import MemoryPolicy, compress_messages


def test_compression_keeps_recent_context():
    messages = ["old " * 100, "middle " * 100, "recent important"]
    compressed = compress_messages(messages, max_chars=80)
    assert "recent important" in compressed
    assert len(compressed) <= 82


def test_policy_has_bounded_memory():
    policy = MemoryPolicy()
    assert policy.short_term_turns > 0
    assert policy.long_term_limit > 0
