"""Tests for the configuration validator and the HubSpot payloads. Run with: pytest -q"""

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from apply_to_hubspot import pipeline_payload, plan_and_apply, property_payload  # noqa: E402
from config_loader import load_all  # noqa: E402
from validate_config import validate  # noqa: E402

CONFIG = load_all()


def test_current_configuration_is_valid():
    assert validate(CONFIG) == []


def test_rejects_property_name_that_is_not_snake_case():
    bad = copy.deepcopy(CONFIG)
    bad["properties"]["contacts"][0]["internal_name"] = "BuyerPersona"
    assert any("snake_case" in e for e in validate(bad))


def test_rejects_title_case_label():
    bad = copy.deepcopy(CONFIG)
    bad["properties"]["companies"][0]["label"] = "Company Segment"
    assert any("Sentence case" in e for e in validate(bad))


def test_rejects_probabilities_that_go_down():
    bad = copy.deepcopy(CONFIG)
    stages = bad["pipelines"]["deals"][0]["stages"]
    stages[0]["probability"], stages[1]["probability"] = 0.5, 0.2
    assert any("must increase" in e for e in validate(bad))


def test_rejects_segment_with_unknown_option():
    bad = copy.deepcopy(CONFIG)
    bad["segments"][2]["filter"] = "customer_health = 'red'"
    assert any("not an option" in e for e in validate(bad))


def test_bool_becomes_checkbox_with_yes_no():
    prop = next(p for p in CONFIG["properties"]["deals"] if p["type"] == "bool")
    payload = property_payload("deals", prop)
    assert payload["fieldType"] == "booleancheckbox"
    assert [o["value"] for o in payload["options"]] == ["true", "false"]


def test_ticket_pipeline_uses_ticket_state():
    payload = pipeline_payload("tickets", CONFIG["pipelines"]["tickets"][0])
    assert {s["metadata"]["ticketState"] for s in payload["stages"]} == {"OPEN", "CLOSED"}


class FakeClient:
    """Simula um portal onde uma propriedade e um pipeline já existem."""

    def __init__(self):
        self.created = []

    def property_exists(self, obj, name):
        return name == "deal_mrr"

    def create_property(self, obj, payload):
        self.created.append(payload["name"])

    def pipeline_labels(self, obj):
        return {"New business"} if obj == "deals" else set()

    def create_pipeline(self, obj, payload):
        self.created.append(payload["label"])


def test_dry_run_changes_nothing_and_skips_existing():
    client = FakeClient()
    summary = plan_and_apply(client, CONFIG, apply=False)
    assert client.created == []
    assert summary["skipped"] == 2


def test_apply_is_idempotent_for_existing_items():
    client = FakeClient()
    plan_and_apply(client, CONFIG, apply=True)
    assert "deal_mrr" not in client.created
    assert "New business" not in client.created
    assert "Customer onboarding" in client.created
