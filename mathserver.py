from mcp.server.fastmcp import FastMCP
from typing import Union

mcp = FastMCP("Math")

@mcp.tool()
def add(a: Union[int, str], b: Union[int, str]) -> int:
    """Add two numbers"""
    return int(a) + int(b)

@mcp.tool()
def subtract(a: Union[int, str], b: Union[int, str]) -> int:
    """Subtract two numbers"""
    return int(a) - int(b)

@mcp.tool()
def multiply(a: Union[int, str], b: Union[int, str]) -> int:
    """Multiply two numbers"""
    return int(a) * int(b)

@mcp.tool()
def divide(a: Union[int, str], b: Union[int, str]) -> float:
    """Divide two numbers"""
    # Guard against division by zero if you like
    return int(a) / int(b)

if __name__ == "__main__":
    # use stdio transport to connect with your MCP client
    mcp.run(transport="stdio")
