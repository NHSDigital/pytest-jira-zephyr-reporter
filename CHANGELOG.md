# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-26

### Changed
- **BREAKING**: Migrated from `requests` to `httpx` with HTTP/2 support
  - Replaced all `requests` library usage with `httpx`
  - Enabled HTTP/2 protocol support for improved performance
  - Updated exception handling to use `httpx` exception types:
    - `requests.exceptions.HTTPError` → `httpx.HTTPStatusError`
    - `requests.exceptions.ConnectionError` → `httpx.ConnectError`
    - `requests.exceptions.Timeout` → `httpx.TimeoutException`
    - `requests.exceptions.RequestException` → `httpx.HTTPError`
  - Updated dependency in `pyproject.toml` to `httpx[http2]>=0.24.0`

### Added
- Added `close()` method to `JiraClient` for proper resource cleanup
- Added context manager support (`__enter__`/`__exit__`) to `JiraClient` for automatic cleanup
- Updated documentation examples to use `httpx`

### Migration Notes
- Users upgrading from v0.1.x should reinstall dependencies: `pip install -U pytest-jira-zephyr-reporter`
- No API changes - the migration is transparent to end users
- All existing functionality remains the same

## [0.1.0] - Initial Release

### Added
- Initial release of pytest-jira-zephyr-reporter
- Automatic test result reporting to Jira
- Integration with Zephyr Squad/Scale test management
- Support for test case creation and execution tracking
- Screenshot attachment support for failures
- Configurable via environment variables
- Background reporting thread (non-blocking)
- Rate limiting and retry logic
- pytest plugin auto-registration

[0.2.0]: https://github.com/NHSDigital/pytest-jira-zephyr-reporter/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/NHSDigital/pytest-jira-zephyr-reporter/releases/tag/v0.1.0
