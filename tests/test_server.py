"""Tests for the Jenkins MCP Server."""

import pytest
from jenkins_mcp.server import JenkinsMCPServer


@pytest.fixture
def server():
    """Create a server instance for testing."""
    return JenkinsMCPServer()


def test_server_initialization(server):
    """Test server initializes correctly."""
    assert server.name == "jenkins-mcp-server"
    assert server.version == "0.1.0"


def test_get_tools(server):
    """Test getting available tools."""
    tools = server.get_tools()
    assert isinstance(tools, dict)
    assert "get_jenkins_status" in tools
    assert "list_jobs" in tools
    assert "get_job_info" in tools
    assert "trigger_job" in tools


def test_process_tool_call_get_jenkins_status(server):
    """Test processing get_jenkins_status tool call."""
    result = server.process_tool_call(
        "get_jenkins_status",
        {"jenkins_url": "http://localhost:8081"}
    )
    assert result["success"] is True
    assert result["result"]["status"] == "healthy"


def test_process_tool_call_list_jobs(server):
    """Test processing list_jobs tool call."""
    result = server.process_tool_call(
        "list_jobs",
        {"jenkins_url": "http://localhost:8081"}
    )
    assert result["success"] is True
    assert "jobs" in result["result"]


def test_process_tool_call_unknown_tool(server):
    """Test processing unknown tool call."""
    result = server.process_tool_call(
        "unknown_tool",
        {}
    )
    assert result["success"] is False
    assert "Unknown tool" in result["error"]
