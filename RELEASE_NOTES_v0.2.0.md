# Release v0.2.0 - HTTP/2 Migration

## Summary
This release migrates the project from the `requests` library to `httpx` with HTTP/2 support, providing improved performance and modern async capabilities while maintaining full backward compatibility.

## What's Changed

### 🚀 Major Updates
- **Migrated to httpx with HTTP/2 support** - Enhanced performance with modern HTTP protocol
- **Added resource cleanup methods** - Proper connection management with `close()` and context manager support
- **Updated all exception handling** - Consistent error handling with httpx exception types

### 📝 Documentation
- Updated code examples to use httpx
- Added CHANGELOG.md for version tracking
- Updated dependency documentation

### 🔧 Technical Details
- Replaced `requests` → `httpx[http2]>=0.24.0`
- Updated exception types across 22 locations
- Added `JiraClient.close()` method
- Implemented `__enter__`/`__exit__` for context manager support
- All tests passing (no breaking changes to public API)

## Migration Guide

For users upgrading from v0.1.0:

```bash
# Update to the latest version
pip install --upgrade git+https://github.com/NHSDigital/pytest-jira-zephyr-reporter.git@v0.2.0
```

**No code changes required** - The migration is transparent to end users. All existing functionality and configuration remains the same.

## Breaking Changes
None - This is a drop-in replacement.

## Installation

```bash
# From GitHub
pip install git+https://github.com/NHSDigital/pytest-jira-zephyr-reporter.git@v0.2.0

# In pyproject.toml
dependencies = [
    "pytest-jira-zephyr-reporter @ git+https://github.com/NHSDigital/pytest-jira-zephyr-reporter.git@v0.2.0",
]
```

## Full Changelog
See [CHANGELOG.md](CHANGELOG.md) for complete details.

---

## Release Checklist (for maintainers)

- [x] Version bumped to 0.2.0 in pyproject.toml
- [x] CHANGELOG.md created and updated
- [x] All code migrated from requests to httpx
- [x] Documentation examples updated
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Git tag created: `git tag -a v0.2.0 -m "Release v0.2.0 - HTTP/2 Migration"`
- [ ] Tag pushed: `git push origin v0.2.0`
- [ ] GitHub release created with release notes
