from weekly_changes import notes

OLD = "| [A](https://x/a) | 1.0k | MIT |\n| [B](https://x/b) | 50 | MIT |\n"
NEW = "| [A](https://x/a) | 1.5k | MIT |\n| 🟢 [C](https://x/c) | 10 | MIT |\n"


def test_added_removed_and_growth():
    out = notes(OLD, NEW)
    assert "C (https://x/c)" in out
    assert "### Removed\n- B" in out
    assert "A: 1,000 → 1,500 (+500)" in out


def test_no_change_is_empty():
    assert notes(OLD, OLD) == ""
