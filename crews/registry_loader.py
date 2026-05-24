"""Registry loader — reads agents + crews from registry.yaml."""
from __future__ import annotations

from pathlib import Path
import yaml

REGISTRY_PATH = Path(__file__).parent / "registry.yaml"


def load_registry() -> dict:
    """Load agents list and crew roster from registry.yaml."""
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"registry.yaml not found at {REGISTRY_PATH}")
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_agent(agent_id: str) -> dict:
    registry = load_registry()
    for a in registry["agents"]:
        if a["id"] == agent_id:
            return a
    raise KeyError(f"Agent '{agent_id}' not found in registry.yaml")


def get_crew_agents(crew_name: str) -> list[dict]:
    registry = load_registry()
    crew_ids = registry["crews"].get(crew_name, [])
    return [get_agent(aid) for aid in crew_ids]


def list_all_agents() -> list[dict]:
    return load_registry()["agents"]


def get_voting_rules() -> dict:
    return load_registry()["voting"]


def get_execution_config() -> dict:
    return load_registry()["execution"]
