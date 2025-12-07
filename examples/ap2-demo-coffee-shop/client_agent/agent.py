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
"""Root agent configuration for the coffee shop client."""

import httpx
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

from client_agent.coffee_client_agent import CoffeeClientAgent

# Remote agent addresses
REMOTE_AGENT_ADDRESSES = [
    "http://localhost:10000/agents/coffee_shop_agent",
]


def create_root_agent():
    """Creates and returns the root agent for the coffee shop client."""
    # Create shared HTTP client
    async_client = httpx.AsyncClient(timeout=30)

    # Create RemoteA2aAgent instances for each remote agent
    remote_agents = []
    for address in REMOTE_AGENT_ADDRESSES:
        agent_card_url = f"{address}/.well-known/agent-card.json"
        agent_name = address.split("/")[-1]
        remote_agents.append(
            RemoteA2aAgent(
                name=agent_name,
                agent_card=agent_card_url,
                httpx_client=async_client,
            )
        )

    # Create the coffee client agent
    client_agent = CoffeeClientAgent(
        remote_agents=remote_agents,
        http_client=async_client,
    )

    return client_agent.create_agent()


# Export the root agent for ADK
root_agent = create_root_agent()

