def test_always_passes() -> None:
    """A trivial passing test to validate successful Jira reporting."""
    assert True


def test_always_fails() -> None:
    """A trivial failing test to validate failed Jira reporting."""
    raise AssertionError("Intentional failure for Jira reporting verification")
