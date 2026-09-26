from app.rate_limit import SlidingWindowLimiter


def test_sliding_window_blocks_after_limit():
    limiter = SlidingWindowLimiter(limit=2, window_seconds=10)
    assert limiter.allow("user", now=0)
    assert limiter.allow("user", now=1)
    assert not limiter.allow("user", now=2)
    assert limiter.allow("user", now=11)
