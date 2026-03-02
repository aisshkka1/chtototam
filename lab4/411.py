import json

def apply_patch(s, p):
    for key, val in patch.items():
        if val is None:
            source.pop(key, None)
        elif key in source and isinstance(source[key], dict) and isinstance(val, dict):
            apply_patch(source[key], val)
        else:
            source[key] = val
    return source

s = json.loads(input())
p = json.loads(input())

result = apply_patch(source, patch)

print(json.dumps(result, separators=(',', ':'), sort_keys=True))
