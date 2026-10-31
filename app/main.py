import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

from app.tools.weather import mcp

mcp_app = mcp.http_app()

app = FastAPI(
    title="Demo MCP Application",
    description="FastAPI application with MCP tools",
    version="1.0.0",
    lifespan=mcp_app.lifespan,
)

app.mount("", mcp_app)


class RootResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str


@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(message="FastAPI and MCP server running successfully")


@app.get("/health", response_model=HealthResponse)
async def health_status() -> HealthResponse:
    return HealthResponse(status="Health")


def main() -> None:
    port: int = int(os.environ.get("PORT", "8080"))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
    )
