# import pytest


def test_always_passes() -> None:
    """A trivial passing test to validate successful Jira reporting."""
    assert True


# Uncomment the following test to validate failed Jira reporting.  It is commented out
# to avoid failing the unit test step on CD.
# @pytest.mark.xfail(reason="Intentional failure for Jira reporting verification")
# def test_always_fails() -> None:
#     """A trivial failing test to validate failed Jira reporting."""
#     raise AssertionError("Intentional failure for Jira reporting verification")
