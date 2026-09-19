# Proposal manifest

Use `proposal-manifest.json` as the commercial source of truth. Keep amounts in minor currency units so installment math is exact.

```json
{
  "schema_version": 1,
  "agreement_version": "2026-09-19-v1",
  "client": {
    "display_name": "Example Builders",
    "legal_name": null,
    "decision_makers": ["Name"]
  },
  "provider": {
    "display_name": "BlendMode",
    "legal_name": "Blend Mode Creative, Inc."
  },
  "engagement": {
    "name": "Acquisition System",
    "objective": "A measurable path from qualified demand to sales meetings",
    "scope_now": ["Landing page", "Lead routing"],
    "later_or_excluded": ["Broad SEO program"]
  },
  "commercial": {
    "currency": "usd",
    "setup_amount": 750000,
    "setup_options": [
      {"id": "full", "label": "Pay in full", "installments": 1, "amount_each": 750000, "checkout_url": null},
      {"id": "three_pay", "label": "Three payments", "installments": 3, "amount_each": 250000, "checkout_url": null}
    ],
    "monthly_fee": 200000,
    "monthly_starts": "at signing",
    "paid_media": {
      "billing_mode": "platform_direct",
      "working_budget": 300000,
      "platforms": ["Google", "Meta"]
    }
  },
  "acceptance": {
    "typed_signature": true,
    "drawn_signature": true,
    "notification_recipients": ["owner@example.com"]
  },
  "delivery": {
    "repository": null,
    "production_domain": null,
    "deployment_provider": "Vercel"
  },
  "evidence": {
    "verified": [],
    "inferences": [],
    "open_decisions": []
  }
}
```

## Rules

- `agreement_version` is immutable after an acceptance can be recorded. Increment it for any contract change.
- `setup_amount`, `amount_each`, `monthly_fee`, and `working_budget` are integer minor units; for USD, 250000 means $2,500.00.
- Every setup option must total `setup_amount` exactly.
- Use `checkout_url: null` until a live or test checkout is actually created and verified.
- `billing_mode` must be `platform_direct` or `agency_pass_through`. If it is `agency_pass_through`, disclose fees, refund handling, unused funds, and account ownership explicitly in both proposal and agreement.
- Unknown legal names, domains, or checkout URLs may remain `null` during drafting, but must be resolved before the affected production action.
- Evidence entries should identify their source. Do not convert an inference into verified evidence because it appears in proposal copy.
