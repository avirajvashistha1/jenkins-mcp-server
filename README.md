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
