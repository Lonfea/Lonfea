from dataclasses import dataclass

from fastapi import Header, HTTPException
from supabase import Client


@dataclass(frozen=True)
class TenantContext:
    user_id: str
    tenant_id: str
    stripe_customer_id: str | None


def resolve_tenant(
    supabase: Client,
    authorization: str | None,
    tenant_id: str | None,
) -> TenantContext:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Missing X-Tenant-ID.")

    token = authorization.removeprefix("Bearer ").strip()
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid access token.")

    membership = (
        supabase.table("memberships")
        .select("tenant_id, tenants(stripe_customer_id)")
        .eq("tenant_id", tenant_id)
        .eq("user_id", str(user.id))
        .limit(1)
        .execute()
    )
    if not membership.data:
        raise HTTPException(status_code=403, detail="User is not a member of this tenant.")

    tenant = membership.data[0].get("tenants") or {}
    return TenantContext(
        user_id=str(user.id),
        tenant_id=tenant_id,
        stripe_customer_id=tenant.get("stripe_customer_id"),
    )


def tenant_headers(
    authorization: str | None = Header(default=None),
    x_tenant_id: str | None = Header(default=None, alias="X-Tenant-ID"),
) -> tuple[str | None, str | None]:
    return authorization, x_tenant_id
