# Acceptance and payment implementation

Read this when the project includes electronic acceptance, notifications, or checkout.

## Acceptance boundary

The acceptance endpoint should validate required signer fields, the agreement version, the selected payment-plan ID, consent, and the signature payload. Reject unknown plan IDs and stale versions server-side. Rate-limit or otherwise constrain abuse when the stack supports it.

Return success only after the acceptance record and required notification have been durably handled. If recording fails, keep checkout locked and show a useful retry message. Do not claim an email is the system of record unless the user chose that architecture.

The browser receipt should show signer identity, legal entity, plan, timestamp, and version. A local/session copy is a convenience, not the authoritative record.

## Drawn signature

Use pointer events so mouse, touch, and stylus work. Preserve strokes in normalized coordinates so resizing does not distort or erase the drawing. Render for the device pixel ratio, provide a clear action, require a meaningful stroke, and include a visible keyboard-focus state. Treat the signature image as sensitive business data; transmit it only to the acceptance endpoint and approved recipients/storage.

## Checkout routing

Map a stable plan ID to a server-approved checkout URL or session. Never accept an arbitrary checkout URL from the browser. Checkout metadata should include the client identifier, engagement identifier, agreement version, payment-plan ID, and installment position when applicable.

If recurring service begins at signing while setup is split, explain the combined first-month amounts directly. Third-party media budget must be visually separate from agency fees and identify the payee.

## Safe verification

Exercise form validation, plan selection, signature drawing/clearing, responsive canvas behavior, locked checkout state, and URL mapping without submitting a real client acceptance. Verify live payment pages only far enough to confirm amount, currency, description, and mode; do not complete payment.
