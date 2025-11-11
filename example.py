"""Example usage of the Jenkins MCP Server."""

from jenkins_mcp.server import JenkinsMCPServer


def main():
    """Demonstrate the Jenkins MCP Server."""
    
    # Initialize the server
    server = JenkinsMCPServer(
        name="jenkins-mcp-server",
        version="0.1.0"
    )
    
    print(f"Initialized {server.name} v{server.version}")
    print(f"\nAvailable tools:")
    
    # Display available tools
    for tool_name, tool_info in server.get_tools().items():
        print(f"\n  - {tool_name}")
        print(f"    Description: {tool_info['description']}")
        print(f"    Input Schema: {tool_info['inputSchema']}")
    
    # Example: Get Jenkins status
    print("\n" + "="*60)
    print("Example: Get Jenkins Status")
    print("="*60)
    
    result = server.process_tool_call(
        "get_jenkins_status",
        {"jenkins_url": "http://localhost:8080"}
    )
    print(f"Result: {result}")
    
    # Example: List jobs
    print("\n" + "="*60)
    print("Example: List Jobs")
    print("="*60)
    
    result = server.process_tool_call(
        "list_jobs",
        {
            "jenkins_url": "http://localhost:8080",
            "filter": "test"
        }
    )
    print(f"Result: {result}")
    
    # Example: Get job info
    print("\n" + "="*60)
    print("Example: Get Job Info")
    print("="*60)
    
    result = server.process_tool_call(
        "get_job_info",
        {
            "jenkins_url": "http://localhost:8080",
            "job_name": "example-job-1"
        }
    )
    print(f"Result: {result}")
    
    # Example: Trigger job
    print("\n" + "="*60)
    print("Example: Trigger Job")
    print("="*60)
    
    result = server.process_tool_call(
        "trigger_job",
        {
            "jenkins_url": "http://localhost:8080",
            "job_name": "example-job-1",
            "parameters": {"BUILD_ENV": "staging"}
        }
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
