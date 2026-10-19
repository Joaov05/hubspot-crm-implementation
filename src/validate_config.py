"""
Validates the CRM configuration before anything is applied to HubSpot.

Checks naming conventions, duplicates, dropdown options, links to requirements,
pipeline probabilities and segment filters. Exits with code 1 if any rule fails,
so it can run in CI on every change.

Usage:  python src/validate_config.py
"""

import re
import sys

from config_loader import load_all

SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
REQUIREMENT_ID = re.compile(r"^R\d+$")
ALLOWED_TYPES = {"string", "number", "currency_number", "enumeration", "bool", "date", "datetime"}
ACCESS_LEVELS = {"edit_all", "edit_team", "edit_own", "view_all", "view_own", "none"}

# propriedades padrão do HubSpot que os filtros de segmento podem usar
STANDARD_PROPERTIES = {
    "contacts": {"lifecyclestage", "hubspot_owner_id", "hs_lead_status", "email"},
    "companies": {"lifecyclestage", "hubspot_owner_id", "domain", "industry"},
}


def validate_properties(properties: dict) -> list[str]:
    errors = []
    for obj, props in properties.items():
        seen = set()
        for p in props:
            name = p.get("internal_name", "<missing>")
            where = f"{obj}.{name}"
            if not SNAKE_CASE.match(name):
                errors.append(f"{where}: internal name must be snake_case")
            if name in seen:
                errors.append(f"{where}: duplicated internal name")
            seen.add(name)
            for field in ("label", "type", "owner", "description", "requirement"):
                if not p.get(field):
                    errors.append(f"{where}: missing '{field}'")
            if p.get("type") not in ALLOWED_TYPES:
                errors.append(f"{where}: invalid type '{p.get('type')}'")
            if p.get("requirement") and not REQUIREMENT_ID.match(p["requirement"]):
                errors.append(f"{where}: requirement must look like R1, R2...")
            label = p.get("label", "")
            # Sentence case: só a primeira letra maiúscula (siglas como MQL/MRR/ERP são permitidas)
            words = label.split()[1:]
            if any(w[0].isupper() and not w.isupper() for w in words if w[0].isalpha()):
                errors.append(f"{where}: label '{label}' must be Sentence case")
            if p.get("type") == "enumeration":
                options = p.get("options") or []
                if len(options) < 2:
                    errors.append(f"{where}: dropdown needs at least 2 options")
                values = [o[0] for o in options]
                if len(values) != len(set(values)):
                    errors.append(f"{where}: duplicated option values")
                for v in values:
                    if not SNAKE_CASE.match(v):
                        errors.append(f"{where}: option value '{v}' must be snake_case")
    return errors


def validate_pipelines(pipelines: dict) -> list[str]:
    errors = []
    for obj, items in pipelines.items():
        for pipe in items:
            where = f"pipeline '{pipe['label']}'"
            stages = pipe.get("stages", [])
            labels = [s["label"] for s in stages]
            if len(labels) != len(set(labels)):
                errors.append(f"{where}: duplicated stage labels")
            if obj == "deals":
                probs = [s["probability"] for s in stages]
                open_probs = [p for p in probs if 0 < p < 1]
                if open_probs != sorted(open_probs):
                    errors.append(f"{where}: open stage probabilities must increase")
                if 1.0 not in probs or 0.0 not in probs:
                    errors.append(f"{where}: needs a won (1.0) and a lost (0.0) stage")
            else:
                states = {s.get("state") for s in stages}
                if not {"OPEN", "CLOSED"} <= states:
                    errors.append(f"{where}: needs at least one OPEN and one CLOSED stage")
            for s in stages:
                if not s.get("entry"):
                    errors.append(f"{where} / {s['label']}: missing entry criteria")
    return errors


def validate_segments(segments: list, properties: dict) -> list[str]:
    errors = []
    for seg in segments:
        obj = seg["object"]
        if not re.match(r"^\[[A-Za-z ]+\] ", seg["name"]):
            errors.append(f"segment '{seg['name']}': name must start with [Team]")
        known = {p["internal_name"] for p in properties.get(obj, [])} | STANDARD_PROPERTIES.get(obj, set())
        # nomes de propriedade usados no filtro (palavras antes de um operador)
        used = re.findall(r"([a-z_]+)\s*(?:=|!=|>=|<=|>|<|IS)", seg["filter"])
        for prop in used:
            if prop not in known:
                errors.append(f"segment '{seg['name']}': unknown property '{prop}'")
        # valores de dropdown usados no filtro precisam existir nas opções
        for prop, value in re.findall(r"([a-z_]+)\s*=\s*'([a-z_]+)'", seg["filter"]):
            custom = next((p for p in properties.get(obj, []) if p["internal_name"] == prop), None)
            if custom and custom.get("options") and value not in [o[0] for o in custom["options"]]:
                errors.append(f"segment '{seg['name']}': '{value}' is not an option of {prop}")
    return errors


def validate_teams(teams: dict) -> list[str]:
    errors = []
    team_names = {t["name"] for t in teams["teams"]}
    cols = teams["permission_columns"]
    for team, levels in teams["permissions"].items():
        if team not in team_names:
            errors.append(f"permissions: unknown team '{team}'")
        if len(levels) != len(cols):
            errors.append(f"permissions: '{team}' must have {len(cols)} access levels")
        for lvl in levels:
            if lvl not in ACCESS_LEVELS:
                errors.append(f"permissions: '{team}' has invalid level '{lvl}'")
    return errors


def validate(config: dict) -> list[str]:
    return (validate_properties(config["properties"])
            + validate_pipelines(config["pipelines"])
            + validate_segments(config["segments"], config["properties"])
            + validate_teams(config["teams"]))


def main() -> None:
    config = load_all()
    errors = validate(config)
    n_props = sum(len(v) for v in config["properties"].values())
    n_pipes = sum(len(v) for v in config["pipelines"].values())
    if errors:
        print(f"{len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"Configuration OK: {n_props} properties, {n_pipes} pipelines, "
          f"{len(config['segments'])} segments, {len(config['teams']['teams'])} teams.")


if __name__ == "__main__":
    main()
