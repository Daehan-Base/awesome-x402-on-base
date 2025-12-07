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
"""Base agent interface for the coffee shop demo."""

from abc import ABC, abstractmethod

from a2a.types import AgentCard


class BaseAgent(ABC):
    """Abstract base class for agent implementations."""

    @abstractmethod
    def create_agent(self):
        """Create and return the ADK agent instance."""
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def create_agent_card(self, url: str) -> AgentCard:
        """Create and return the AgentCard for this agent."""
        raise NotImplementedError("Subclasses must implement this method")

