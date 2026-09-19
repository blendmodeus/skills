#!/usr/bin/env python3
"""Validate the commercial invariants in a proposal-manifest.json file."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


VERSION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-v\d+$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def require_string(errors: list[str], value: object, path: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(errors, f"{path} must be a non-empty string")


def require_minor_units(errors: list[str], value: object, path: str, *, allow_zero: bool = False) -> None:
    minimum = 0 if allow_zero else 1
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        fail(errors, f"{path} must be an integer in minor currency units")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_proposal_manifest.py proposal-manifest.json", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if data.get("schema_version") != 1:
        fail(errors, "schema_version must be 1")

    version = data.get("agreement_version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        fail(errors, "agreement_version must match YYYY-MM-DD-vN")

    for section in ("client", "provider", "engagement", "commercial", "acceptance", "delivery", "evidence"):
        if not isinstance(data.get(section), dict):
            fail(errors, f"{section} must be an object")

    client = data.get("client", {})
    provider = data.get("provider", {})
    engagement = data.get("engagement", {})
    commercial = data.get("commercial", {})
    acceptance = data.get("acceptance", {})

    require_string(errors, client.get("display_name"), "client.display_name")
    require_string(errors, provider.get("display_name"), "provider.display_name")
    require_string(errors, engagement.get("name"), "engagement.name")
    require_string(errors, engagement.get("objective"), "engagement.objective")

    currency = commercial.get("currency")
    if not isinstance(currency, str) or not re.fullmatch(r"[a-z]{3}", currency):
        fail(errors, "commercial.currency must be a lowercase ISO currency code")

    setup_amount = commercial.get("setup_amount")
    require_minor_units(errors, setup_amount, "commercial.setup_amount")
    require_minor_units(errors, commercial.get("monthly_fee"), "commercial.monthly_fee", allow_zero=True)

    options = commercial.get("setup_options")
    if not isinstance(options, list) or not options:
        fail(errors, "commercial.setup_options must contain at least one option")
    else:
        ids: set[str] = set()
        for index, option in enumerate(options):
            prefix = f"commercial.setup_options[{index}]"
            if not isinstance(option, dict):
                fail(errors, f"{prefix} must be an object")
                continue
            option_id = option.get("id")
            require_string(errors, option_id, f"{prefix}.id")
            if isinstance(option_id, str):
                if option_id in ids:
                    fail(errors, f"{prefix}.id duplicates {option_id!r}")
                ids.add(option_id)
            installments = option.get("installments")
            amount_each = option.get("amount_each")
            require_minor_units(errors, installments, f"{prefix}.installments")
            require_minor_units(errors, amount_each, f"{prefix}.amount_each")
            if isinstance(installments, int) and not isinstance(installments, bool) and isinstance(amount_each, int) and not isinstance(amount_each, bool) and isinstance(setup_amount, int):
                if installments * amount_each != setup_amount:
                    fail(errors, f"{prefix} totals {installments * amount_each}, not setup_amount {setup_amount}")
            checkout_url = option.get("checkout_url")
            if checkout_url is not None and (not isinstance(checkout_url, str) or not checkout_url.startswith("https://")):
                fail(errors, f"{prefix}.checkout_url must be null or an https URL")

    paid_media = commercial.get("paid_media")
    if paid_media is not None:
        if not isinstance(paid_media, dict):
            fail(errors, "commercial.paid_media must be null or an object")
        else:
            if paid_media.get("billing_mode") not in {"platform_direct", "agency_pass_through"}:
                fail(errors, "commercial.paid_media.billing_mode must be platform_direct or agency_pass_through")
            require_minor_units(errors, paid_media.get("working_budget"), "commercial.paid_media.working_budget", allow_zero=True)

    recipients = acceptance.get("notification_recipients")
    if not isinstance(recipients, list) or not recipients:
        fail(errors, "acceptance.notification_recipients must contain at least one email")
    else:
        for email in recipients:
            if not isinstance(email, str) or not EMAIL_RE.fullmatch(email):
                fail(errors, f"invalid notification recipient: {email!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {path} is internally consistent ({version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
