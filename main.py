from parsers.uml_parser import parse_uml_model
from parsers.generators import generate_meta_json, generate_config_xml
from parsers.config_diff import generate_delta_json, apply_delta
import json
import os

INPUT_XML = "input/impulse_test_input.xml"
CONFIG_JSON = "input/config.json"
PATCHED_CONFIG_JSON = "input/patched_config.json"
OUT_DIR = "out"

os.makedirs(OUT_DIR, exist_ok=True)

if __name__ == "__main__":
    uml_classes, uml_aggs = parse_uml_model(INPUT_XML)

    # 1. meta.json
    meta = generate_meta_json(uml_classes)
    with open(f"{OUT_DIR}/meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    # 2. config.xml
    config_xml = generate_config_xml(uml_classes, uml_aggs)
    with open(f"{OUT_DIR}/config.xml", "w") as f:
        f.write(config_xml)

    # 3. delta.json
    with open(CONFIG_JSON) as f:
        config = json.load(f)
    with open(PATCHED_CONFIG_JSON) as f:
        patched_config = json.load(f)

    delta = generate_delta_json(config, patched_config)
    with open(f"{OUT_DIR}/delta.json", "w") as f:
        json.dump(delta, f, indent=2)

    # 4. res_patched_config.json
    result = apply_delta(config, delta)
    with open(f"{OUT_DIR}/res_patched_config.json", "w") as f:
        json.dump(result, f, indent=2)
