"""Loads the YAML configuration files from config/."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"


def load(name: str):
    # lê um arquivo de configuração, ex.: load("properties")
    with open(CONFIG_DIR / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_all() -> dict:
    return {
        "properties": load("properties"),
        "pipelines": load("pipelines"),
        "segments": load("segments"),
        "teams": load("teams_and_permissions"),
    }
