---
name: client-proposal-builder
description: Build and safely launch a branded prospective-client proposal site that carries one deal from sales evidence through scope, agreement, electronic signature, notifications, and the matching checkout. Use when creating or revising a client proposal microsite, contract-and-payment flow, or reusable proposal template; do not use for a standalone sales email or a contract that will not be implemented as a site.
metadata:
  version: "1.0.0"
  short-description: Build client proposal-to-payment sites
---

# Client Proposal Builder

Build one coherent commercial path: proposal → agreement → acceptance → payment. Treat the deal brief as the source of truth and make every public surface reconcile to it.

## Start with the deal record

Reconstruct the latest deal state from the sources the user authorizes. Separate verified facts, explicit client choices, and unresolved decisions. Do not silently fill material commercial or legal gaps from an older email, proposal, or similar client.

Create `proposal-manifest.json` at the project root before implementation. Read [references/proposal-manifest.md](references/proposal-manifest.md) for the schema and rules. Ask only about unresolved fields that would materially change scope, price, authority, billing, contract language, notification routing, or deployment.

## Build the experience

Use the client's actual brand assets and a restrained visual system derived from them. The proposal should explain the client-specific problem, outcome, first build, sequencing, investment, boundaries, responsibilities, and next action. Avoid generic agency language, decorative symbols that turn into emoji, and design choices that interfere with copying, printing, or mobile use.

The agreement must be plain-language and consistent with the proposal. Include the parties, scope, exclusions, fees, payment timing, client dependencies, ownership, confidentiality, term/termination, limitation language appropriate to the deal, and governing terms supplied or approved by the user. Do not represent generated language as legal advice.

When acceptance and checkout are in scope, read [references/acceptance-and-payment.md](references/acceptance-and-payment.md) before implementing them.

## Preserve the commercial invariants

- Use one agreement version across the page metadata, acceptance record, notification, checkout metadata, and receipt.
- Keep proposal, agreement, checkout amounts, installment math, and payment timing identical.
- State who pays third-party spend. Default paid media to client-owned accounts billed directly by the platforms unless the deal explicitly says otherwise.
- Signing records acceptance; it does not itself charge the client. Unlock the checkout matching the selected payment option after successful acceptance recording.
- Collect typed signer identity and a drawn signature when an electronic-signature flow is requested. Record signer name, title, email, legal entity, selected plan, UTC timestamp, version, and signature image.
- Send acceptance notifications only to the recipients in the manifest. Attach the drawn signature when the provider supports it. Never put secret keys in the repository or browser bundle.
- Any agreement change after launch requires a new version and must not restore an acceptance from an older version.
- Do not execute a real signature or payment while testing.

## External mutations

Building the site does not by itself authorize sending client messages, signing, charging, modifying DNS, creating live payment links, or deploying production. Use existing configured accounts only within the user's authorization. Preview safely first; obtain the missing authority before any additional external mutation.

For live payment links, preserve client, engagement, agreement version, and payment-plan metadata. For production deployment, use a client-specific repository and domain, confirm secret environment variables exist without exposing them, and verify the custom domain resolves to the intended deployment.

## Validate and release

Run:

From the generated project, run the validator from this skill's installed directory:

```bash
python <skill-root>/scripts/validate_proposal_manifest.py proposal-manifest.json
```

Then follow [references/release-checklist.md](references/release-checklist.md). Verify desktop and mobile, the full selection/signature/notification/checkout routing logic without submitting a real acceptance, and the deployed custom domain. Report which external actions were performed and which were deliberately not performed.
