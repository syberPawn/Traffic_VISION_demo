from __future__ import annotations

import json

from src.config import REGISTRY_PATH


def ensure_registry_file() -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not REGISTRY_PATH.exists():
        REGISTRY_PATH.write_text(json.dumps({"owners": []}, indent=2), encoding="utf-8")


def load_owners() -> list[dict[str, str]]:
    ensure_registry_file()
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {"owners": []}

    owners = data.get("owners", [])
    return owners if isinstance(owners, list) else []


def save_owner(name: str, phone: str, email: str) -> None:
    owners = load_owners()
    owners.append(
        {
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip(),
        }
    )
    REGISTRY_PATH.write_text(json.dumps({"owners": owners}, indent=2), encoding="utf-8")
