"""
Applies the configuration (properties and pipelines) to a HubSpot portal.

- Dry run by default: prints the plan and changes nothing.
- Idempotent: anything that already exists is skipped, so it is safe to run again.
- Needs a private app token with CRM schema scopes in the HUBSPOT_ACCESS_TOKEN
  environment variable. Use a test or sandbox portal first.

Usage:
    python src/apply_to_hubspot.py            # show the plan
    python src/apply_to_hubspot.py --apply    # create what is missing
"""

import argparse
import os
import sys

import requests

from config_loader import load_all
from validate_config import validate

API = "https://api.hubapi.com"
OBJECT_IDS = {"contacts": "contacts", "companies": "companies", "deals": "deals", "tickets": "tickets"}
GROUPS = {"contacts": "contactinformation", "companies": "companyinformation", "deals": "dealinformation"}


def property_payload(obj: str, prop: dict) -> dict:
    # traduz o YAML para o formato da API de propriedades do HubSpot
    kind = prop["type"]
    payload = {
        "name": prop["internal_name"],
        "label": prop["label"],
        "description": prop["description"],
        "groupName": GROUPS[obj],
    }
    if kind == "enumeration":
        payload.update(type="enumeration", fieldType="select", options=[
            {"value": v, "label": label, "displayOrder": i}
            for i, (v, label) in enumerate(prop["options"])
        ])
    elif kind == "bool":
        payload.update(type="enumeration", fieldType="booleancheckbox", options=[
            {"value": "true", "label": "Yes", "displayOrder": 0},
            {"value": "false", "label": "No", "displayOrder": 1},
        ])
    elif kind == "currency_number":
        payload.update(type="number", fieldType="number", showCurrencySymbol=True)
    elif kind == "number":
        payload.update(type="number", fieldType="number")
    elif kind in ("date", "datetime"):
        payload.update(type=kind, fieldType="date")
    else:
        payload.update(type="string", fieldType="text")
    return payload


def pipeline_payload(obj: str, pipe: dict) -> dict:
    stages = []
    for i, s in enumerate(pipe["stages"]):
        if obj == "deals":
            metadata = {"probability": str(s["probability"])}
        else:
            metadata = {"ticketState": s["state"]}
        stages.append({"label": s["label"], "displayOrder": i, "metadata": metadata})
    return {"label": pipe["label"], "displayOrder": 1, "stages": stages}


class HubSpotClient:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}",
                                     "Content-Type": "application/json"})

    def property_exists(self, obj: str, name: str) -> bool:
        r = self.session.get(f"{API}/crm/v3/properties/{obj}/{name}")
        if r.status_code == 404:
            return False
        r.raise_for_status()
        return True

    def create_property(self, obj: str, payload: dict) -> None:
        self.session.post(f"{API}/crm/v3/properties/{obj}", json=payload).raise_for_status()

    def pipeline_labels(self, obj: str) -> set[str]:
        r = self.session.get(f"{API}/crm/v3/pipelines/{obj}")
        r.raise_for_status()
        return {p["label"] for p in r.json().get("results", [])}

    def create_pipeline(self, obj: str, payload: dict) -> None:
        self.session.post(f"{API}/crm/v3/pipelines/{obj}", json=payload).raise_for_status()


def plan_and_apply(client, config: dict, apply: bool) -> dict:
    summary = {"created": 0, "skipped": 0}
    # ---- propriedades
    for obj, props in config["properties"].items():
        for prop in props:
            name = prop["internal_name"]
            if client.property_exists(OBJECT_IDS[obj], name):
                print(f"  = {obj}.{name} already exists")
                summary["skipped"] += 1
                continue
            print(f"  + {obj}.{name} ({prop['type']})")
            if apply:
                client.create_property(OBJECT_IDS[obj], property_payload(obj, prop))
            summary["created"] += 1
    # ---- pipelines (comparados pelo nome)
    for obj, pipes in config["pipelines"].items():
        existing = client.pipeline_labels(OBJECT_IDS[obj])
        for pipe in pipes:
            if pipe["label"] in existing:
                print(f"  = pipeline '{pipe['label']}' already exists")
                summary["skipped"] += 1
                continue
            print(f"  + pipeline '{pipe['label']}' ({len(pipe['stages'])} stages)")
            if apply:
                client.create_pipeline(OBJECT_IDS[obj], pipeline_payload(obj, pipe))
            summary["created"] += 1
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="create missing items (default: dry run)")
    args = parser.parse_args()

    config = load_all()
    errors = validate(config)
    if errors:
        sys.exit("Configuration is invalid. Run src/validate_config.py first.")

    token = os.environ.get("HUBSPOT_ACCESS_TOKEN")
    if not token:
        sys.exit("Set HUBSPOT_ACCESS_TOKEN with a private app token (test portal).")

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"[{mode}] Rotalog CRM configuration")
    summary = plan_and_apply(HubSpotClient(token), config, args.apply)
    verb = "created" if args.apply else "to create"
    print(f"\n{summary['created']} {verb}, {summary['skipped']} already in place.")


if __name__ == "__main__":
    main()
