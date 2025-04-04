#!/usr/bin/env python3

from typing import Dict, List, Optional, Any, TypedDict, Union
from mcp.server.fastmcp import FastMCP, Context

# Define the Sequential Thinking server
mcp = FastMCP("Sequential Thinking")

# Store thought history
thought_history = []
thought_branches = {}

@mcp.tool()
def sequential_thinking(
    thought: str,
    thoughtNumber: int,
    totalThoughts: int,
    nextThoughtNeeded: bool,
    isRevision: Optional[bool] = None,
    revisesThought: Optional[int] = None,
    branchFromThought: Optional[int] = None,
    branchId: Optional[str] = None,
    needsMoreThoughts: Optional[bool] = None,
    ctx: Context = None
) -> str:
    """
    Facilitates a detailed, step-by-step thinking process for problem-solving and analysis.
    
    Args:
        thought: The current thinking step
        thoughtNumber: Current thought number
        totalThoughts: Estimated total thoughts needed
        nextThoughtNeeded: Whether another thought step is needed
        isRevision: Whether this revises previous thinking
        revisesThought: Which thought is being reconsidered
        branchFromThought: Branching point thought number
        branchId: Branch identifier
        needsMoreThoughts: If more thoughts are needed
        ctx: MCP context
    
    Returns:
        Response message about the recorded thought
    """
    # Create thought data structure
    thought_data = {
        "thought": thought,
        "thoughtNumber": thoughtNumber,
        "totalThoughts": totalThoughts,
        "nextThoughtNeeded": nextThoughtNeeded,
        "isRevision": isRevision,
        "revisesThought": revisesThought,
        "branchFromThought": branchFromThought,
        "branchId": branchId,
        "needsMoreThoughts": needsMoreThoughts
    }
    
    # Handle branching
    if branchId:
        if branchFromThought:
            # Starting a new branch
            if branchId not in thought_branches:
                # Find the thought to branch from in the main history
                branch_from_index = next(
                    (i for i, t in enumerate(thought_history) 
                     if t["thoughtNumber"] == branchFromThought), 
                    None
                )
                
                if branch_from_index is not None:
                    # Create a new branch with thoughts up to the branch point
                    thought_branches[branchId] = thought_history[:branch_from_index + 1].copy()
                else:
                    # Branch point not found, create empty branch
                    thought_branches[branchId] = []
        
        # Add thought to the branch
        if branchId in thought_branches:
            # Handle revision in branch
            if isRevision and revisesThought:
                revise_index = next(
                    (i for i, t in enumerate(thought_branches[branchId]) 
                     if t["thoughtNumber"] == revisesThought),
                    None
                )
                if revise_index is not None:
                    thought_branches[branchId][revise_index] = thought_data
            else:
                thought_branches[branchId].append(thought_data)
    else:
        # Handle revision in main history
        if isRevision and revisesThought:
            revise_index = next(
                (i for i, t in enumerate(thought_history) 
                 if t["thoughtNumber"] == revisesThought),
                None
            )
            if revise_index is not None:
                thought_history[revise_index] = thought_data
        else:
            thought_history.append(thought_data)
    
    # Format response
    if isRevision:
        return f"Revised thought {revisesThought}."
    
    if branchId:
        branch_text = f" (Branch: {branchId})"
    else:
        branch_text = ""
        
    if nextThoughtNeeded:
        if needsMoreThoughts:
            return f"Recorded thought {thoughtNumber}/{totalThoughts}{branch_text}. More thoughts will be needed."
        else:
            return f"Recorded thought {thoughtNumber}/{totalThoughts}{branch_text}. Continue with the next thought."
    else:
        return f"Recorded final thought {thoughtNumber}/{totalThoughts}{branch_text}. The thinking process is complete."

@mcp.resource("thoughts://history")
def get_thought_history() -> str:
    """
    Get the complete thought history as a formatted string.
    
    Returns:
        Formatted thought history
    """
    if not thought_history:
        return "No thoughts recorded yet."
    
    result = "# Thought History\n\n"
    for i, thought in enumerate(thought_history):
        result += f"## Thought {thought['thoughtNumber']}/{thought['totalThoughts']}\n\n"
        result += f"{thought['thought']}\n\n"
    
    return result

@mcp.resource("thoughts://branches/{branch_id}")
def get_branch_thoughts(branch_id: str) -> str:
    """
    Get the thoughts for a specific branch.
    
    Args:
        branch_id: The branch identifier
    
    Returns:
        Formatted branch thoughts
    """
    if branch_id not in thought_branches:
        return f"Branch '{branch_id}' not found."
    
    if not thought_branches[branch_id]:
        return f"No thoughts recorded for branch '{branch_id}'."
    
    result = f"# Branch: {branch_id}\n\n"
    for i, thought in enumerate(thought_branches[branch_id]):
        result += f"## Thought {thought['thoughtNumber']}/{thought['totalThoughts']}\n\n"
        result += f"{thought['thought']}\n\n"
    
    return result

@mcp.resource("thoughts://summary")
def get_thought_summary() -> str:
    """
    Get a summary of all thoughts and branches.
    
    Returns:
        Summary of thoughts and branches
    """
    result = "# Sequential Thinking Summary\n\n"
    
    result += "## Main Thought Line\n\n"
    result += f"- Total thoughts: {len(thought_history)}\n"
    if thought_history:
        result += f"- Current progress: Thought {thought_history[-1]['thoughtNumber']}/{thought_history[-1]['totalThoughts']}\n"
    
    if thought_branches:
        result += "\n## Branches\n\n"
        for branch_id, branch in thought_branches.items():
            result += f"- Branch '{branch_id}': {len(branch)} thoughts\n"
    
    return result

@mcp.prompt()
def thinking_process_guide() -> str:
    """
    Guide for using the sequential thinking process.
    """
    return """
    # Sequential Thinking Process Guide
    
    This tool helps break down complex problems into manageable steps through a structured thinking process.
    
    ## How to Use
    
    1. Start with an initial thought (thoughtNumber = 1)
    2. Continue adding thoughts sequentially
    3. You can revise previous thoughts if needed
    4. You can create branches to explore alternative paths
    
    ## Example
    
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
    """

def main():
    """Entry point for the Sequential Thinking MCP server."""
    print("Starting Sequential Thinking MCP server...")
    mcp.run()

if __name__ == "__main__":
    main()
