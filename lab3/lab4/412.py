import json
import sys

def serialize(val):
    if val == "<missing>":
        return "<missing>"
    return json.dumps(val, separators=(',', ':'))

def deep_diff(obj1, obj2, path=""):
    diffs = []

    keys = set()
    if isinstance(obj1, dict):
        keys.update(obj1.keys())
    if isinstance(obj2, dict):
        keys.update(obj2.keys())

    for key in keys:
        new_path = f"{path}.{key}" if path else key
        val1 = obj1.get(key, "<missing>") if isinstance(obj1, dict) else "<missing>"
        val2 = obj2.get(key, "<missing>") if isinstance(obj2, dict) else "<missing>"

        if isinstance(val1, dict) and isinstance(val2, dict):
            diffs.extend(deep_diff(val1, val2, new_path))
        else:
            if val1 != val2:
                diffs.append(f"{new_path} : {serialize(val1)} -> {serialize(val2)}")

    return diffs

obj1 = json.loads(sys.stdin.readline())
obj2 = json.loads(sys.stdin.readline())

differences = deep_diff(obj1, obj2)

if differences:
    for d in sorted(differences):
        print(d)
else:
    print("No differences")