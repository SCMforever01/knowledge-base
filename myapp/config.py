import json
from typing import Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, 'r') as file:
        return json.load(file)