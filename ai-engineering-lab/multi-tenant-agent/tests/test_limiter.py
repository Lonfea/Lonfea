from app.limiter import TenantLimiter


def test_tenants_have_independent_quotas():
    limiter = TenantLimiter(limit=1, window_seconds=60)
    assert limiter.allow("tenant-a", now=0)
    assert not limiter.allow("tenant-a", now=1)
    assert limiter.allow("tenant-b", now=1)
