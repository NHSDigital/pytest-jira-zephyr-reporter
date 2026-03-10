# pytest-jira-zephyr-reporter

A generic pytest plugin for automated test result reporting to Jira using Zephyr Squad/Scale test management.

## Features

- ✅ Automatic test result reporting to Jira
- ✅ Creates test cases if they don't exist
- ✅ Links test executions to test cycles
- ✅ Screenshot attachment support for failures
- ✅ Configurable via environment variables
- ✅ Background reporting thread (non-blocking)
- ✅ Rate limiting and retry logic built-in
- ✅ Works with any Jira instance using Zephyr

## Installation

Install from GitHub:

```bash
pip install git+https://github.com/NHSDigital/pytest-jira-zephyr-reporter.git@v0.1.0
```

Or add to your `pyproject.toml`:

```toml
dependencies = [
    "pytest-jira-zephyr-reporter @ git+https://github.com/NHSDigital/pytest-jira-zephyr-reporter.git@v0.1.0",
]
```

The plugin will automatically register with pytest via entry points.

## How It Works

When pytest tests run, this plugin automatically:
1. Searches for a Jira test case matching the test name
2. Creates a new test case if one doesn't exist
3. Creates a test execution in the specified test cycle
4. Updates the execution status based on the test result (PASS/FAIL/SKIPPED)
5. Attaches screenshots for failed tests (if available)

## Configuration

All environment variables below are **required** for the plugin to work. If any are missing or invalid, the integration will be disabled and tests will run without Jira reporting.

```bash
export JIRA_INTEGRATION_ENABLED=true
export JIRA_REPORTING_URL=https://your-jira-instance.atlassian.net
export JIRA_API_TOKEN=your-api-token
export JIRA_PROJECT_KEY=PROJ
export ZEPHYR_PROJECT_ID=10001
export JIRA_TEST_CYCLE_VERSION="v1.0.0"
```

### Environment Variables

- `JIRA_INTEGRATION_ENABLED` - Enable/disable integration (default: `true`)
- `JIRA_REPORTING_URL` - **Required**. Base URL of your Jira instance
- `JIRA_API_TOKEN` - **Required**. Jira API token for authentication
- `JIRA_PROJECT_KEY` - **Required**. Project key (e.g., PROJ, MYAPP)
- `ZEPHYR_PROJECT_ID` - **Required**. Numeric Zephyr project ID
- `JIRA_TEST_CYCLE_VERSION` - Test cycle version (default: "Unscheduled")
- `JIRA_TEST_CYCLE_KEY` - Optional. Specific test cycle key to use
- `SCREENSHOT_ALL_STEPS` - Take screenshots for all steps, not just failures (default: `false`)
- `JIRA_MAX_RETRIES` - Maximum API retry attempts (default: `3`)
- `JIRA_TIMEOUT` - API request timeout in seconds (default: `30`)
- `JIRA_MIN_REQUEST_INTERVAL` - Minimum seconds between API requests (default: `0.1`)

## Usage

Once installed and configured, the plugin works automatically. Simply run your pytest tests:

```bash
pytest
```

To disable Jira reporting temporarily:

```bash
export JIRA_INTEGRATION_ENABLED=false
pytest
```

## Architecture

The package consists of:

- **config.py** - Configuration management from environment variables
- **models.py** - Data models and result mapping
- **client.py** - Jira/Zephyr REST API client with rate limiting
- **reporter.py** - Main reporter logic and background thread
- **hooks.py** - Pytest hooks integration (auto-registered)

### Initialization

The plugin initializes at the start of the pytest session (`pytest_configure` hook):
1. Loads configuration from environment variables
2. Validates all required fields are present
3. Creates an authenticated Jira client
4. Looks up or creates the test cycle
5. If any step fails, the integration is disabled with a log message

This "fail fast" approach ensures configuration errors are caught immediately before any tests run.

### Background Reporting

Test results are reported asynchronously in a background thread to avoid blocking test execution. The thread processes a queue of test results and handles retries automatically.

## API Endpoints Used

### Jira REST API (v2)
- `GET /rest/api/2/issue/{issueKey}` - Get issue details
- `POST /rest/api/2/issue` - Create test cases
- `GET /rest/api/2/search` - Search for test cases by name

### Zephyr Squad API
- `GET /rest/zapi/latest/cycle` - Get test cycles
- `POST /rest/zapi/latest/execution` - Create test execution
- `PUT /rest/zapi/latest/execution/{executionId}/execute` - Update status
- `GET /rest/zapi/latest/util/testExecutionStatus` - Get status IDs

## Result Mapping

| Pytest Outcome | Jira/Zephyr Status |
|----------------|-------------------|
| passed         | PASS              |
| failed         | FAIL              |
| skipped        | UNEXECUTED        |

## Disabling Integration

The plugin can be disabled by setting:

```bash
export JIRA_INTEGRATION_ENABLED=false
```

The integration will also be automatically disabled if:
- Any required environment variable is missing or empty
- The specified test cycle is not found/cannot be created
- Authentication fails
- Any API connection error occurs during initialization

When disabled, tests will run normally without Jira reporting, and you'll see a log message explaining why.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/NHSDigital/pytest-jira-zephyr-reporter.git
cd pytest-jira-zephyr-reporter

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .
```

## License

MIT License - see LICENSE file for details.

## Support

For issues, questions, or contributions, please use the [GitHub Issues](https://github.com/NHSDigital/pytest-jira-zephyr-reporter/issues) page.
