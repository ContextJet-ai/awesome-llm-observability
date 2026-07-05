import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from pii_scrub import find_pii, scrub  # noqa: E402


def test_masks_email_and_ssn():
    out = scrub("mail a@b.com and ssn 123-45-6789")
    assert "a@b.com" not in out and "<email>" in out
    assert "123-45-6789" not in out and "<ssn>" in out


def test_valid_card_is_masked():
    # 4111 1111 1111 1111 is a Luhn-valid test card.
    assert scrub("card 4111 1111 1111 1111") == "card <card>"


def test_luhn_invalid_number_is_not_masked():
    # 16 ones fail the Luhn check, so this is not treated as a card.
    assert "<card>" not in scrub("order id 1111111111111111")


def test_clean_text_unchanged():
    text = "the quick brown fox jumps over 42 lazy dogs"
    assert scrub(text) == text


def test_find_pii_reports_entities():
    found = dict(find_pii("a@b.com card 4111111111111111"))
    assert found.get("email") == "a@b.com"
    assert "card" in found


def test_empty_input():
    assert scrub("") == ""
    assert find_pii("") == []
