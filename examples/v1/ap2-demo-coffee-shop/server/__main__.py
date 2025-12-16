# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main entry point for the coffee shop server."""

import asyncio
import logging
import os

import click
import uvicorn
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from server.agents.routes import create_agent_routes

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def homepage(request):
    """Root endpoint with server info."""
    return PlainTextResponse(
        "☕ AI Coffee Shop Server\n\n"
        "Available endpoints:\n"
        "  - /agents/coffee_shop_agent/.well-known/agent-card.json\n"
        "  - /agents/coffee_shop_agent (A2A RPC endpoint)\n\n"
        "Use the client agent to place orders!"
    )


async def health_check(request):
    """Health check endpoint."""
    return PlainTextResponse("OK")


def create_app(host: str, port: int) -> Starlette:
    """Creates and configures the Starlette application."""
    base_url = f"http://{host}:{port}"
    base_path = "/agents"

    async def startup():
        """Initialize agent routes on startup."""
        logger.info("☕ Starting AI Coffee Shop Server...")
        logger.info(f"   Base URL: {base_url}")
        
        agent_routes = await create_agent_routes(base_url, base_path)
        app.routes.extend(agent_routes)
        
        logger.info("✅ Server ready!")
        logger.info(f"   Agent Card: {base_url}{base_path}/coffee_shop_agent/.well-known/agent-card.json")

    # CORS middleware for cross-origin requests
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    # Base routes
    routes = [
        Route("/", homepage),
        Route("/health", health_check),
    ]

    app = Starlette(
        debug=True,
        routes=routes,
        middleware=middleware,
        on_startup=[startup],
    )

    return app


@click.command()
@click.option("--host", default="localhost", help="Host to bind to")
@click.option("--port", default=10000, help="Port to bind to")
def main(host: str, port: int):
    """Run the AI Coffee Shop server."""
    print("\n" + "=" * 50)
    print("☕ AI Coffee Shop - AP2 & x402 Demo")
    print("=" * 50 + "\n")

    # Check required environment variables
    if not os.getenv("MERCHANT_WALLET_ADDRESS"):
        print("⚠️  Warning: MERCHANT_WALLET_ADDRESS not set")
        print("   Payments will fail without a valid wallet address.\n")

    if not os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_GENAI_USE_VERTEXAI") != "TRUE":
        print("⚠️  Warning: GOOGLE_API_KEY not set")
        print("   Get one from: https://aistudio.google.com/apikey\n")

    app = create_app(host, port)
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    main()

