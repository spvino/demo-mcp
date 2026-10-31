import logging
import random

import httpx
from fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="Demo MCP Server",
    instructions="A demo MCP server for testing purpose only",
)


@mcp.tool(
    name="sum_of_two_nonumber",
    description="Calculate the sum of two numbers",
)
async def calculate_sum(num1: float, num2: float) -> str:
    """Calculate the sum of two numbers."""
    logger.info("Tool called: calculate_sum(%s, %s)", num1, num2)
    return f"Sum of {num1} and {num2} is: {num1 + num2}"


@mcp.tool(
    name="secret-word",
    description="Find a random secret word",
)
async def get_secret_word() -> str:
    """Get a random secret word."""
    logger.info("Tool called: get_secret_word()")
    return random.choice(["Apple", "Banana", "Mongo", "Duriyan"])


@mcp.tool(
    name="get-weather",
    description="Get current weather for a city",
)
async def get_weather(city: str) -> str:
    """Get weather data for a specified city."""
    logger.info("Tool called: get_weather(%s)", city)
    url = f"https://wttr.in/{city}?format=j1"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            current = data["current_condition"][0]
            temperature = current["temp_C"]
            description = current["weatherDesc"][0]["value"]

            return f"Current weather in {city}: {description}, {temperature}C"
    except (httpx.HTTPError, ValueError, KeyError, IndexError):
        logger.error("Weather API failed")
        return f"Unable to fetch weather for {city}"
