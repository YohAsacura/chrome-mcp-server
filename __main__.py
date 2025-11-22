"""
Chrome MCP Server - Main entry point

Usage:
    python -m src.server

For development:
    python src/server.py
"""

from src.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
