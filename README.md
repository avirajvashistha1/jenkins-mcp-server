"""README for Jenkins MCP Server."""

# Jenkins MCP Server

A Python-based Model Context Protocol (MCP) server for Jenkins integration.

## Overview

This MCP server provides tools for interacting with Jenkins CI/CD systems, enabling:
- Jenkins server status monitoring
- Job listing and filtering
- Job information retrieval
- Job triggering with parameters

## Features

- **Get Jenkins Status**: Monitor Jenkins server health
- **List Jobs**: Retrieve jobs from a Jenkins server with optional filtering
- **Get Job Info**: Obtain detailed information about a specific job
- **Trigger Job**: Trigger job builds with optional parameters

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd jenkins-mcp-server
```

2. Install in development mode:
```bash
pip install -e ".[dev]"
```

## Usage

### Running the Server

```bash
python -m jenkins_mcp.server
```

### Using in Your Application

```python
from jenkins_mcp.server import JenkinsMCPServer

# Initialize the server
server = JenkinsMCPServer()

# Get available tools
tools = server.get_tools()

# Call a tool
result = server.process_tool_call(
    "get_jenkins_status",
    {"jenkins_url": "http://localhost:8080"}
)
```

### Tool Schema

Each tool has a defined input schema. For example:

**get_jenkins_status**:
```json
{
  "jenkins_url": "string (required)"
}
```

**list_jobs**:
```json
{
  "jenkins_url": "string (required)",
  "filter": "string (optional)"
}
```

**get_job_info**:
```json
{
  "jenkins_url": "string (required)",
  "job_name": "string (required)"
}
```

**trigger_job**:
```json
{
  "jenkins_url": "string (required)",
  "job_name": "string (required)",
  "parameters": "object (optional)"
}
```

## server.py — functionality details

`jenkins_mcp/server.py` implements the MCP server and exposes a small set of tools
to interact with a Jenkins instance. This section documents the behavior, inputs,
outputs and notable runtime behavior so integrators can use the tools reliably.

Tools implemented (summary):
- `get_jenkins_status` — quick health/status check for a Jenkins URL.
- `list_jobs` — returns a simple list of jobs (supports a `filter` argument).
- `get_job_info` — returns basic information about a specific job.
- `trigger_job` — triggers a Jenkins job and performs robust tracking (queue -> build -> console).

`trigger_job` details
- Inputs (arguments object):
  - `jenkins_url` (string, required) — base URL of the Jenkins server (e.g. `http://localhost:8081`).
  - `job_name` (string, required) — the job to trigger (e.g. `my-pipeline`).
  - `parameters` (object, optional) — parameters for parameterized jobs.
  - `username` / `api_token` (optional) — optional credentials; when not supplied the server will
    attempt to read `JENKINS_USERNAME` and `JENKINS_API_TOKEN` from environment variables (a
    minimal `.env` loader is included for local development).

- Behavior:
  - Performs a POST to either `/job/<job>/build` or `/job/<job>/buildWithParameters` depending on
    whether `parameters` were provided.
  - If credentials are present, it attempts to fetch a Jenkins CSRF crumb from
    `/crumbIssuer/api/json` and includes it in the trigger request headers.
  - After triggering, if Jenkins returns a `Location` header pointing to a queue item,
    the server polls the queue item's `/api/json` until an `executable` with a `number`
    (build number) is attached.
  - Once a build number is found the server polls the build `/api/json` until the
    `building` field becomes `false` (finished) or a timeout is reached.
  - When the build is available (or after polling), the server attempts to fetch
    `/consoleText` to return the console output (best-effort).

- Outputs: the handler returns a dictionary containing at least the following keys:
  - `triggered` (bool) — whether the trigger request returned a 2xx code.
  - `status_code` (int | None) — status code of the trigger HTTP request.
  - `api_response` (object) — parsed JSON or an error message from the trigger response.
  - `api_response_text` (string) — safe stringified representation of `api_response` for logging.
  - `queue_url` (string | None) — the queue item URL if present.
  - `queue_item` (object | None) — JSON payload of the queue item when available.
  - `build_number` (int | None) — the Jenkins build number when discovered.
  - `build_url` (string | None) — the build URL when discovered.
  - `console_output` (string) — best-effort fetch of `/consoleText`.

- Error and timeout handling:
  - Crumb fetching is best-effort; if it fails the trigger still proceeds and Jenkins
    will respond accordingly.
  - Queue and build polling loops are bounded (short timeouts). If polling fails to
    find an executable/build before the timeout the handler returns the data it
    has collected so far (including `api_response_text` and any `queue_url`).

Example usage (Python):

```python
from jenkins_mcp.server import JenkinsMCPServer
server = JenkinsMCPServer()
res = server.process_tool_call("trigger_job", {
    "jenkins_url": "http://localhost:8081",
    "job_name": "jenkins-mcp-server-build",
})
print(res["result"] if res.get("success") else res)
```

Notes
- The implementation is intentionally minimal and dependency-light (uses `requests`).
- For local credential convenience the project includes a tiny `.env` loader which
  will populate `JENKINS_USERNAME` and `JENKINS_API_TOKEN` if a `.env` file exists.
  Remember not to commit `.env` — the repository `.gitignore` already ignores it.

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=jenkins_mcp
```

## Development

### Code Quality

Format code with Black:
```bash
black jenkins_mcp tests
```

Lint with Ruff:
```bash
ruff check jenkins_mcp tests
```

Type check with mypy:
```bash
mypy jenkins_mcp
```

### Project Structure

```
jenkins-mcp-server/
├── jenkins_mcp/
│   ├── __init__.py
│   └── server.py          # Main server implementation
├── tests/
│   └── test_server.py     # Test suite
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## MCP Protocol Integration

This server implements the Model Context Protocol (MCP) specification. To use it with MCP clients:

1. Ensure the server is running
2. Configure your MCP client to connect to this server
3. The client will discover available tools through the protocol
4. Use the tools as defined in the protocol

## Future Enhancements

- Add actual Jenkins API integration
- Support Jenkins authentication (API tokens, OAuth)
- Add build log streaming
- Add pipeline support
- Add build artifact management
- Add user and permission management

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
