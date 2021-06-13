def get_environment_keyval(values: [str]) -> [dict]:
    key_val: [dict] = []
    for val in values:
        key_val.append({
            "name": "Production" if val == "default" else val,
            "value": val
        })
    return key_val

def get_keyval(key: str, values: [dict]) -> [dict]:
    key_val: [dict] = []
    for val in values:
        key_val.append({ "name": val[key], "value": val[key] })
    return key_val

def validate_context_request(context: dict):
    """Validates if context input is consistent"""
    
    missing = []
    if context.get("environment", None) is None:
        missing.append("Environment")

    if context.get("group", None) is None:
        missing.append("Group")

    if context.get("status", None) is None:
        missing.append("Status")

    error = " - ".join([str(elem) for elem in missing])
    if len(missing):
        raise Exception(f"Missing [{error}]")