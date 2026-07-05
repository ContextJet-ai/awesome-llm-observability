"""
pii_scrub - mask common PII in text before it reaches a tracing backend.

Pure-Python, zero dependencies. Detects emails, credit cards (Luhn-validated to
cut false positives), US SSNs, phone numbers, IPv4 addresses, and IBANs, and
replaces them with typed placeholders. A safe default for observability
redaction - for high-stakes/finance use, layer a real detector (Presidio,
LLM Guard) on top.

    from pii_scrub import scrub, find_pii

    scrub("email me at a@b.com, card 4111111111111111")
    # -> "email me at <email>, card <card>"

CC0 - ContextJet.ai.
"""

from __future__ import annotations

import re

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_PHONE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")
_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
_CARD_CAND = re.compile(r"\b(?:\d[ -]?){13,19}\b")


def _luhn_ok(digits: str) -> bool:
    """Luhn checksum - real card numbers pass, most random digit runs don't."""
    total, alt = 0, False
    for ch in reversed(digits):
        d = ord(ch) - 48
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


def _mask_cards(text: str) -> str:
    def repl(m):
        digits = re.sub(r"[ -]", "", m.group())
        return "<card>" if 13 <= len(digits) <= 19 and _luhn_ok(digits) else m.group()
    return _CARD_CAND.sub(repl, text)


def scrub(text: str) -> str:
    """Return text with detected PII replaced by typed placeholders."""
    if not text:
        return text
    text = _EMAIL.sub("<email>", text)
    text = _mask_cards(text)          # before phone/ssn so long card runs match first
    text = _IBAN.sub("<iban>", text)
    text = _SSN.sub("<ssn>", text)
    text = _PHONE.sub("<phone>", text)
    text = _IPV4.sub("<ip>", text)
    return text


def find_pii(text: str):
    """Return a list of (type, value) detected, without mutating text."""
    found = []
    for typ, rx in (("email", _EMAIL), ("ssn", _SSN), ("phone", _PHONE),
                    ("ip", _IPV4), ("iban", _IBAN)):
        found += [(typ, m.group()) for m in rx.finditer(text)]
    for m in _CARD_CAND.finditer(text):
        digits = re.sub(r"[ -]", "", m.group())
        if 13 <= len(digits) <= 19 and _luhn_ok(digits):
            found.append(("card", m.group()))
    return found


if __name__ == "__main__":
    sample = "hi, ssn 123-45-6789, card 4111 1111 1111 1111, mail a@b.com, call 415-555-0199"
    print(scrub(sample))
