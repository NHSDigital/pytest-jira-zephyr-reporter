"""Test-only hook to send pass/fail outcomes to Jira during teardown."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import pytest

from pytest_jira_zephyr_reporter.reporter import JiraTestReporter

logger = logging.getLogger(__name__)
_demo_reporter: JiraTestReporter | None = None


def _load_env_file() -> None:
    """Load KEY=VALUE pairs from repository .env into process environment."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        logger.info("No .env file found at %s", env_path)
        return

    loaded_count = 0
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[7:].strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue

        # Preserve explicit environment values over .env defaults.
        if key not in os.environ:
            os.environ[key] = value
            loaded_count += 1

    logger.info("Loaded %d variable(s) from .env", loaded_count)


_load_env_file()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Initialize a reporter for these demo tests.

    This test hook is skipped when the package plugin is already active,
    to avoid duplicate Jira reporting.
    """
    global _demo_reporter  # noqa: PLW0603

    if config.pluginmanager.hasplugin("jira_zephyr_reporter"):
        logger.info("Built-in jira_zephyr_reporter plugin is active; using it directly")
        _demo_reporter = None
        return

    _demo_reporter = JiraTestReporter(is_xdist_worker=False)
    if _demo_reporter.is_enabled():
        logger.info("Test hook Jira reporter enabled")
    else:
        logger.info("Test hook Jira reporter disabled due to configuration")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, _call: pytest.CallInfo[None]):
    """Capture the call-phase report for teardown reporting."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item: pytest.Item) -> None:
    """Send pass/fail results to Jira for each test item."""
    if not _demo_reporter or not _demo_reporter.is_enabled():
        return

    rep_call = getattr(item, "rep_call", None)
    if rep_call is None:
        return

    docstring = item.function.__doc__ if getattr(item, "function", None) else ""
    test_case_key = _demo_reporter.get_or_create_test_case(item.nodeid, docstring or "")
    if not test_case_key:
        logger.warning("Could not resolve Jira test case for %s", item.nodeid)
        return

    jira_result = _demo_reporter.pytest_result_to_jira_result(rep_call.outcome)
    error_message = str(rep_call.longrepr) if rep_call.failed else None
    _demo_reporter.report_test_result(
        test_case_key=test_case_key,
        result=jira_result,
        error_message=error_message,
    )
