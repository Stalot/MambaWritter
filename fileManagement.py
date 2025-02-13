from pathlib import Path
import json
import sys

def bundle_path(path: str | Path) -> Path:
    bundle_dir = Path(getattr(sys, '_MEIPASS', Path.cwd()))
    config_path = bundle_dir / path
    return config_path

def read_json(filepath: str | Path) -> dict:
    with open(filepath, "r") as json_file:
        data: dict = json.loads(json_file.read())
    return data

if __name__ == "__main__":
    path = bundle_path("cache/custom_app_settings.json")
    print(path)