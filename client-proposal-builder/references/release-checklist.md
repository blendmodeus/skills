# Release checklist

## Commercial integrity

- Proposal, agreement, manifest, notifications, and checkout show the same version and economics.
- Installment totals and combined monthly amounts are correct.
- Paid media or other pass-through costs identify the payee and account owner.
- Included work, later work, client responsibilities, and dependencies are unambiguous.

## Acceptance

- Signer identity, legal entity, title, email, consent, selected plan, UTC timestamp, version, typed signature, and drawn signature are handled as designed.
- Stale acceptance state cannot unlock a revised agreement.
- Failed recording keeps payment locked.
- Approved recipients receive the intended fields and signature attachment; no unintended recipient is present.

## Experience

- Header and footer end at the document bounds; no overscroll-colored blank page appears.
- Logo, primary action, pricing, payment choices, and signature canvas work at narrow mobile widths and desktop widths.
- Text contains no accidental emoji presentation or copy/paste artifacts.
- Focus, labels, error messages, contrast, and reduced-motion behavior are usable.
- Print/PDF output excludes interactive controls and preserves agreement content.

## Production

- Secrets are environment variables, not committed files or client JavaScript.
- Repository and deployment target are client-specific and clean of unrelated changes.
- Custom domain resolves to the latest intended production deployment.
- Payment links are in the intended test/live mode and carry matching metadata.
- Browser console and server logs show no relevant errors.
- No real acceptance, notification, message, or payment was triggered by QA unless the user explicitly authorized that test.
