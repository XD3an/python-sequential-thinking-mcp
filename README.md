# Sequential Thinking MCP Server (Python Implementation)

<p align="left">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </a>
</p>



A Python implementation of the Sequential Thinking MCP server using the official Model Context Protocol (MCP) Python SDK. This server facilitates a detailed, step-by-step thinking process for problem-solving and analysis.

## Features

- Break down complex problems into manageable steps
- Revise and refine thoughts as understanding deepens
- Branch into alternative paths of reasoning
- Adjust the total number of thoughts dynamically
- Generate and verify solution hypotheses

## Usage

### Running Directly

```bash
uv --directory "/path/to/sequential-thinking-mcp" run main.py
```

### Development Mode

For development and testing, you can use the MCP CLI tools:

```bash
# Install MCP CLI tools
pip install "mcp[cli]"

# Run in development mode
mcp dev "/path/to/sequential-thinking-mcp"

# npx @modelcontextprotocol/inspector
npx @modelcontextprotocol/inspector uv --diectory "/path/to/sequential-thinking-mcp" run main.py
```

## Integration

```
mcp install "\path\to\sequential-thinking-mcp\server.py"
```

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/sequential-thinking-mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

## Sequential Thinking Tool

The server provides a tool called `sequential_thinking` with the following parameters:

- `thought` (string): The current thinking step
- `thoughtNumber` (integer): Current thought number
- `totalThoughts` (integer): Estimated total thoughts needed
- `nextThoughtNeeded` (boolean): Whether another thought step is needed
- `isRevision` (boolean, optional): Whether this revises previous thinking
- `revisesThought` (integer, optional): Which thought is being reconsidered
- `branchFromThought` (integer, optional): Branching point thought number
- `branchId` (string, optional): Branch identifier
- `needsMoreThoughts` (boolean, optional): If more thoughts are needed

## Resources

The server provides the following resources for accessing thought data:

- `thoughts://history`: Get the complete thought history
- `thoughts://branches/{branch_id}`: Get thoughts for a specific branch
- `thoughts://summary`: Get a summary of all thoughts and branches

## Prompts

- `thinking_process_guide`: Guide for using the sequential thinking process

## Example Usage

```python
# First thought
sequential_thinking(
    thought="First, we need to understand the problem requirements.",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Second thought
sequential_thinking(
    thought="Now, let's analyze the key constraints.",
    thoughtNumber=2,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Revise a thought
sequential_thinking(
    thought="Actually, we need to clarify the problem requirements first.",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True,
    isRevision=True,
    revisesThought=1
)

# Branch from thought 2
sequential_thinking(
    thought="Let's explore an alternative approach.",
    thoughtNumber=3,
    totalThoughts=5,
    nextThoughtNeeded=True,
    branchFromThought=2,
    branchId="alternative-approach"
)
```

## Integration with Claude or Other AI Assistants

To use this server with Claude or other AI assistants that support MCP:

1. Install the MCP server in Claude Desktop using the MCP CLI
2. The AI can then use the sequential_thinking tool to break down complex problems

## About Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a standardized way for applications to provide context and tools to LLMs. It allows:

- **Resources**: Providing contextual data to the LLM
- **Tools**: Exposing functionality for the LLM to take actions
- **Prompts**: Defining reusable templates for LLM interactions

For more information, visit [modelcontextprotocol.io](https://modelcontextprotocol.io)

## License

MIT License. See [LICENSE](LICENSE) for details.
