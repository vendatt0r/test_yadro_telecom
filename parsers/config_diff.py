def generate_delta_json(config, patched):
    additions = {}
    deletions = {}
    updates = {}

    for key in patched:
        if key not in config:
            additions[key] = patched[key]
        elif patched[key] != config[key]:
            updates[key] = patched[key]

    for key in config:
        if key not in patched:
            deletions[key] = config[key]

    return {
        "additions": additions,
        "deletions": deletions,
        "updates": updates
    }

def apply_delta(config, delta):
    result = config.copy()
    result.update(delta["additions"])
    result.update(delta["updates"])
    for key in delta["deletions"]:
        result.pop(key, None)
    return result
