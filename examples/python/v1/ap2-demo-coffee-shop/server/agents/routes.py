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
"""A2A routing configuration for the coffee shop server."""

import os
from typing import Dict, List

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard
from google.adk.agents import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from starlette.routing import BaseRoute, Route

from ._adk_agent_executor import ADKAgentExecutor
from .base_agent import BaseAgent
from .coffee_shop_agent import CoffeeShopAgent
from .x402_executor import CoffeeShopExecutor

# Register agents
AGENTS: Dict[str, BaseAgent] = {
    "coffee_shop_agent": CoffeeShopAgent(),
}


async def create_agent_routes(base_url: str, base_path: str) -> List[BaseRoute]:
    """
    Creates and configures the routes for all registered agents.
    
    Args:
        base_url: Base URL for the server (e.g., "http://localhost:10000")
        base_path: Base path for agents (e.g., "/agents")
    
    Returns:
        List of Starlette routes
    """
    # Validate API key
    if os.getenv("GOOGLE_GENAI_USE_VERTEXAI") != "TRUE" and not os.getenv("GOOGLE_API_KEY"):
        raise ValueError(
            "GOOGLE_API_KEY environment variable not set. "
            "Get one from https://aistudio.google.com/apikey"
        )

    routes: List[BaseRoute] = []

    for path, agent_factory in AGENTS.items():
        full_path = f"{base_path}/{path}"
        url = f"{base_url}{full_path}"

        routes.extend(
            await _create_routes(
                agent_path=path,
                full_path=full_path,
                agent_card=await agent_factory.create_agent_card(url),
                agent=agent_factory.create_agent(),
                artifact_service=InMemoryArtifactService(),
                session_service=InMemorySessionService(),
                memory_service=InMemoryMemoryService(),
            ),
        )

    return routes


async def _create_routes(
    agent_path: str,
    full_path: str,
    agent_card: AgentCard,
    agent: LlmAgent,
    artifact_service: InMemoryArtifactService,
    session_service: InMemorySessionService,
    memory_service: InMemoryMemoryService,
) -> List[Route]:
    """
    Creates routes for a single agent with x402 payment wrapper.
    """
    # Create the ADK runner
    runner = Runner(
        app_name=agent_card.name,
        agent=agent,
        artifact_service=artifact_service,
        session_service=session_service,
        memory_service=memory_service,
    )

    # 1. Create base executor
    agent_executor = ADKAgentExecutor(runner, agent_card)

    # 2. Wrap with x402 executor for payment handling
    agent_executor = CoffeeShopExecutor(agent_executor)

    # 3. Create request handler
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore(),
    )

    # 4. Create A2A application
    a2a_app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    # 5. Generate routes
    agent_card_url = f"{full_path}/.well-known/agent-card.json"
    return a2a_app.routes(agent_card_url=agent_card_url, rpc_url=full_path)

