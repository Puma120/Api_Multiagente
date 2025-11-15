from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Registry of agents by name
_AGENTS: Dict[str, Any] = {}

def register_agents(agent_map: Dict[str, Any]):
    """Register multiple agent instances by name."""
    for name, agent in agent_map.items():
        _AGENTS[name] = agent
        logger.info(f"message_bus: registered agent {name}")

def register_agent(name: str, agent: Any):
    _AGENTS[name] = agent
    logger.info(f"message_bus: registered agent {name}")

def get_agent(name: str):
    return _AGENTS.get(name)

def deliver(message: Dict[str, Any]) -> Dict[str, Any]:
    """Deliver a message to the target agent and return its response.

    Message structure expected:
    {"from": "AgentA", "to": "AgentB", "protocol": "ACP", "type": "MSG_TYPE", "content": {...}}
    """
    to = message.get("to")
    if not to:
        return {"status": "error", "error": "no_recipient"}

    agent = _AGENTS.get(to)
    if not agent:
        logger.warning(f"message_bus: agent '{to}' not found")
        return {"status": "error", "error": "agent_not_found", "agent": to}

    try:
        response = agent.receive_message(message)
        return response if response is not None else {"status": "delivered"}
    except Exception as e:
        logger.exception(f"message_bus: error delivering message to {to}: {e}")
        return {"status": "error", "error": str(e)}
