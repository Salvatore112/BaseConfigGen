import json
from typing import Dict, List, Union
from dataclasses import dataclass


@dataclass
class DeltaItem:
    key: str
    value: str = None
    from_value: str = None
    to_value: str = None


class DeltaProcessor:
    def __init__(self, original_config_path: str, patched_config_path: str):
        self.original_config_path = original_config_path
        self.patched_config_path = patched_config_path

    def _load_config(self, config_path: str) -> Dict[str, str]:
        with open(config_path, "r") as f:
            return json.load(f)

    def generate_delta(self) -> json:
        original = self._load_config(self.original_config_path)
        patched = self._load_config(self.patched_config_path)

        delta = {"additions": [], "deletions": [], "updates": []}

        added_keys = set(patched.keys()) - set(original.keys())
        delta["additions"] = [{"key": key, "value": patched[key]} for key in added_keys]

        deleted_keys = set(original.keys()) - set(patched.keys())
        delta["deletions"] = list(deleted_keys)

        common_keys = set(original.keys()) & set(patched.keys())
        delta["updates"] = [
            {"key": key, "from": original[key], "to": patched[key]}
            for key in common_keys
            if original[key] != patched[key]
        ]

        return json.dumps(delta, indent=4)

    def apply_delta(self) -> json:
        original = self._load_config(self.original_config_path)
        delta = json.loads(self.generate_delta())

        for key in delta["deletions"]:
            original.pop(key, None)

        for update in delta["updates"]:
            original[update["key"]] = update["to"]

        for addition in delta["additions"]:
            original[addition["key"]] = addition["value"]

        return json.dumps(original, indent=4)
