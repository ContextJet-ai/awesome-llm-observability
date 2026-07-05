---
name: scrub-pii-from-text
description: Use this to strip PII (emails, credit cards, SSNs, phone numbers, IPs, IBANs) out of text before it is logged to a tracing backend or sent to a third-party model. Trigger on "redact PII", "scrub sensitive data", "mask PII before logging", "don't send customer data to the tracing tool", especially for finance/healthcare/regulated apps. Ships a runnable, tested scrubber with a Luhn check to cut false positives.
license: CC0-1.0
---

# Scrub PII from text

Observability captures prompts and completions, which in a regulated app can mean shipping account numbers or PII to a third-party backend. This skill ships a scrubber you can run in the export path so raw values never leave your process.

## Use the bundled script

[`scripts/pii_scrub.py`](scripts/pii_scrub.py) is pure Python, no install needed:

```python
from pii_scrub import scrub, find_pii

scrub("email a@b.com, card 4111 1111 1111 1111")   # -> "email <email>, card <card>"
find_pii(text)                                      # [("email", "a@b.com"), ("card", ...)]
```

It masks emails, credit cards (**Luhn-validated**, so random 16-digit order ids are not flagged), US SSNs, phone numbers, IPv4 addresses, and IBANs. Run it directly: `python scripts/pii_scrub.py`.

## How to apply it

1. **Redact before export**, not after: call `scrub()` in your span processor / logging hook so no path bypasses it (see `redact-pii-for-tracing` for where that hook goes).
2. **Redact both directions:** user input and model output (models echo PII back).
3. **Layer a real detector for high stakes:** this is a strong default, but for finance/health, add Presidio or LLM Guard plus a domain ruleset. Regex alone misses context-dependent PII.

## Validation

Run the tests: `pytest skills/scrub-pii-from-text/tests/`. They confirm emails/SSNs/valid cards are masked, that a Luhn-invalid number is left alone (false-positive guard), that clean text is untouched, and that `find_pii` reports entities.

## Anti-patterns

- Regex-only redaction as your whole compliance story for high-stakes data.
- Masking input but not model output.
- Redacting after the SDK already exported the span (mask before export).
