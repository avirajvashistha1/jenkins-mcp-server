"""Main MCP Server implementation for Jenkins integration."""

import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth
from typing import Any, Optional


# Load .env file if present (simple loader, avoids extra dependency)
def _load_dotenv(path: str = None) -> None:
    """Load environment variables from a .env file into os.environ.

    This is a minimal implementation to make local credential configuration easy
    for development. The file should contain lines like KEY=VALUE. Lines starting
    with # are treated as comments.
    """
    p = path or os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    try:
        if os.path.exists(p):
            with open(p, "r", encoding="utf8") as f:
                for raw in f:
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v
    except Exception:
        # Silently ignore env load errors; env vars can still be provided externally
        pass


_load_dotenv()


class JenkinsMCPServer:
    """
    A Model Context Protocol server for Jenkins integration.
    
    This server provides tools for interacting with Jenkins CI/CD systems,
    including job management, build monitoring, and status retrieval.
    """
    
    def __init__(self, name: str = "jenkins-mcp-server", version: str = "0.1.0"):
        """
        Initialize the Jenkins MCP Server.
        
        Args:
            name: The name of the server
            version: The version of the server
        """
        self.name = name
        self.version = version
        self.tools = self._initialize_tools()
    
    def _initialize_tools(self) -> dict[str, dict[str, Any]]:
        """
        Initialize the available tools for the MCP server.
        
        Returns:
            A dictionary containing tool definitions
        """
        return {
            "get_jenkins_status": {
                "description": "Get the current status of a Jenkins server",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "jenkins_url": {
                            "type": "string",
                            "description": "The URL of the Jenkins server"
                        }
                    },
                    "required": ["jenkins_url"]
                }
            },
            "list_jobs": {
                "description": "List all jobs on a Jenkins server",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "jenkins_url": {
                            "type": "string",
                            "description": "The URL of the Jenkins server"
                        },
                        "filter": {
                            "type": "string",
                            "description": "Optional filter pattern for job names"
                        }
                    },
                    "required": ["jenkins_url"]
                }
            },
            "get_job_info": {
                "description": "Get detailed information about a Jenkins job",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "jenkins_url": {
                            "type": "string",
                            "description": "The URL of the Jenkins server"
                        },
                        "job_name": {
                            "type": "string",
                            "description": "The name of the job"
                        }
                    },
                    "required": ["jenkins_url", "job_name"]
                }
            },
            "trigger_job": {
                "description": "Trigger a Jenkins job build",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "jenkins_url": {
                            "type": "string",
                            "description": "The URL of the Jenkins server"
                        },
                        "job_name": {
                            "type": "string",
                            "description": "The name of the job to trigger"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "Optional job parameters"
                        }
                    },
                    "required": ["jenkins_url", "job_name"]
                }
            }
        }
    
    def get_tools(self) -> dict[str, dict[str, Any]]:
        """
        Get all available tools.
        
        Returns:
            A dictionary of tool definitions
        """
        return self.tools
    
    def process_tool_call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Process a tool call request.
        
        Args:
            tool_name: The name of the tool to call
            arguments: The arguments for the tool
            
        Returns:
            The result of the tool call
        """
        if tool_name not in self.tools:
            return {
                "error": f"Unknown tool: {tool_name}",
                "success": False
            }
        
        # Route to the appropriate handler
        handler = getattr(self, f"_handle_{tool_name}", None)
        if handler is None:
            return {
                "error": f"No handler for tool: {tool_name}",
                "success": False
            }
        
        try:
            result = handler(arguments)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def _handle_get_jenkins_status(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Handle get_jenkins_status tool call."""
        jenkins_url = arguments.get("jenkins_url", "http://localhost:8081")
        # Placeholder implementation
        return {
            "jenkins_url": jenkins_url,
            "status": "healthy",
            "message": "Jenkins server is operational, Please note that this is a demo Impl."
        }
    
    def _handle_list_jobs(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Handle list_jobs tool call."""
        jenkins_url = arguments.get("jenkins_url", "http://localhost:8081")
        filter_pattern = arguments.get("filter", "")
        # Placeholder implementation

        return {
            "jenkins_url": jenkins_url,
            "jobs": [
                {"name": "example-job-1", "status": "stable"},
                {"name": "example-job-2", "status": "unstable"}
            ],
            "filter_applied": filter_pattern
        }
    
    def _handle_get_job_info(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Handle get_job_info tool call."""
        jenkins_url = arguments.get("jenkins_url", "http://localhost:8081")
        job_name = arguments.get("job_name")
        # Placeholder implementation
        return {
            "jenkins_url": jenkins_url,
            "job_name": job_name,
            "status": "stable",
            "last_build": 42,
            "last_build_status": "success"
        }
    
    def _handle_trigger_job(self, arguments: dict[str, Any]) -> dict[str, Any]:
        """Handle trigger_job tool call."""
        jenkins_url = arguments.get("jenkins_url", "http://localhost:8081")
        job_name = arguments.get("job_name")
        parameters = arguments.get("parameters", {})

        # Support optional credentials: username + api_token
        # Credentials may be provided in arguments or via environment variables
        username = arguments.get("username") or os.getenv("JENKINS_USERNAME")
        api_token = arguments.get("api_token") or os.getenv("JENKINS_API_TOKEN")
        auth = HTTPBasicAuth(username, api_token) if username and api_token else None

        # Robust trigger implementation:
        # - POST to trigger endpoint
        # - if Location header (queue URL) returned, poll the queue item for an executable
        # - once executable is present, poll the build until finished and fetch console output
        build_endpoint = "buildWithParameters" if parameters else "build"
        api_url = f"{jenkins_url}/job/{job_name}/{build_endpoint}"

        headers: dict[str, str] = {}
        status_code = None
        api_body: dict[str, Any] = {}

        # Try to fetch crumb if auth is present
        if auth:
            try:
                crumb_url = f"{jenkins_url}/crumbIssuer/api/json"
                crumb_resp = requests.get(crumb_url, auth=auth, timeout=10)
                if getattr(crumb_resp, "status_code", None) == 200:
                    cj = crumb_resp.json()
                    crumb_field = cj.get("crumbRequestField")
                    crumb_value = cj.get("crumb")
                    if crumb_field and crumb_value:
                        headers[crumb_field] = crumb_value
            except Exception:
                # proceed without crumb; Jenkins may reject if required
                pass

        # Trigger the build
        try:
            if parameters and build_endpoint == "buildWithParameters":
                response = requests.post(api_url, headers=headers or None, auth=auth, data=parameters, timeout=10)
            else:
                response = requests.post(api_url, headers=headers or None, auth=auth, timeout=10)

            status_code = getattr(response, "status_code", None)
            try:
                api_body = response.json() if status_code and status_code < 400 else {"error": response.text}
            except Exception:
                api_body = {"message": "Triggered (no JSON body)"} if status_code in (200, 201, 202) else {"error": response.text}
        except Exception as exc:
            status_code = None
            api_body = {"error": str(exc)}

        # Tracking variables
        queue_url: Optional[str] = None
        queue_item: Optional[dict[str, Any]] = None
        build_number: Optional[int] = None
        build_url: Optional[str] = None
        console_output = ""

        # If Jenkins returned a Location header, use it to poll the queue
        try:
            location = response.headers.get("Location") or response.headers.get("location")
        except Exception:
            location = None

        if location:
            if location.startswith("/"):
                queue_url = jenkins_url.rstrip("/") + location
            else:
                queue_url = location

            queue_api = queue_url.rstrip("/") + "/api/json"
            for _ in range(30):
                try:
                    qresp = requests.get(queue_api, auth=auth, timeout=10)
                    if getattr(qresp, "status_code", None) == 200:
                        qj = qresp.json()
                        exe = qj.get("executable")
                        if exe and exe.get("number"):
                            build_number = exe.get("number")
                            build_url = exe.get("url") or f"{jenkins_url.rstrip('/')}/job/{job_name}/{build_number}/"
                            queue_item = qj
                            break
                except Exception:
                    pass
                time.sleep(2)

        # If we have a build number, poll the build until finished and fetch console
        if build_url and build_number:
            build_api = build_url.rstrip("/") + "/api/json"
            for _ in range(60):
                try:
                    bresp = requests.get(build_api, auth=auth, timeout=10)
                    if getattr(bresp, "status_code", None) == 200:
                        bj = bresp.json()
                        if not bj.get("building", True):
                            break
                except Exception:
                    pass
                time.sleep(2)

            try:
                console_url = build_url.rstrip("/") + "/consoleText"
                console_resp = requests.get(console_url, auth=auth, timeout=10)
                if getattr(console_resp, "status_code", None) == 200:
                    console_output = console_resp.text
            except Exception:
                console_output = "Unable to fetch console output"

        # Safe stringified api_response
        try:
            api_response_text = json.dumps(api_body, ensure_ascii=False)
        except Exception:
            api_response_text = str(api_body)

        return {
            "jenkins_url": jenkins_url,
            "job_name": job_name,
            "triggered": status_code in (200, 201, 202),
            "status_code": status_code,
            "parameters_sent": parameters,
            "api_response": api_body,
            "api_response_text": api_response_text,
            "queue_url": queue_url,
            "queue_item": queue_item,
            "build_number": build_number,
            "build_url": build_url,
            "console_output": console_output,
        }


def main():
    """Entry point for the MCP server."""
    import argparse
    import requests
    
    parser = argparse.ArgumentParser(description="Jenkins MCP Server")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args()
    
    server = JenkinsMCPServer()
    print(f"Starting {server.name} v{server.version}")
    print(f"Available tools: {list(server.get_tools().keys())}")


if __name__ == "__main__":
    main()
