import subprocess
import pathlib
import json

CONFIG_JSON = pathlib.Path(__file__).parent / "config.jsonc"


def read_json():
    with open(CONFIG_JSON, "r") as f:
        return json.loads(f.read())


print(read_json())
