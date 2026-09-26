create extension if not exists pgcrypto;

create table if not exists public.tenants (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  stripe_customer_id text unique,
  created_at timestamptz not null default now()
);

create table if not exists public.memberships (
  tenant_id uuid not null references public.tenants(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null check (role in ('owner', 'admin', 'member')),
  primary key (tenant_id, user_id)
);

create table if not exists public.usage_events (
  id bigint generated always as identity primary key,
  tenant_id uuid not null references public.tenants(id),
  user_id uuid not null references auth.users(id),
  request_id uuid not null unique,
  units integer not null check (units > 0),
  latency_ms integer not null check (latency_ms >= 0),
  created_at timestamptz not null default now()
);

create table if not exists public.audit_events (
  id bigint generated always as identity primary key,
  tenant_id uuid not null references public.tenants(id),
  user_id uuid not null references auth.users(id),
  request_id uuid,
  event_type text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

alter table public.tenants enable row level security;
alter table public.memberships enable row level security;
alter table public.usage_events enable row level security;
alter table public.audit_events enable row level security;

create or replace function public.is_tenant_member(target_tenant uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.memberships m
    where m.tenant_id = target_tenant
      and m.user_id = (select auth.uid())
  );
$$;

create policy tenant_select on public.tenants
for select to authenticated
using (public.is_tenant_member(id));

create policy membership_select on public.memberships
for select to authenticated
using (user_id = (select auth.uid()));

create policy usage_select on public.usage_events
for select to authenticated
using (public.is_tenant_member(tenant_id));

create policy audit_select on public.audit_events
for select to authenticated
using (public.is_tenant_member(tenant_id));

revoke all on table public.tenants, public.memberships, public.usage_events, public.audit_events
from anon;
