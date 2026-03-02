import json
import re
import sys

# Read JSON
data = json.loads(sys.stdin.readline())

# Number of queries
q = int(sys.stdin.readline())

# Pattern to split keys and indices
pattern = re.compile(r'\.?([a-zA-Z_]\w*)|\[(\d+)\]')

for _ in range(q):
    query = sys.stdin.readline().strip()
    current = data
    found = True

    # Extract all keys and indices
    for key, idx in pattern.findall(query):
        if key:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                found = False
                break
        elif idx:
            i = int(idx)
            if isinstance(current, list) and 0 <= i < len(current):
                current = current[i]
            else:
                found = False
                break

    if found:
        print(json.dumps(current, separators=(',', ':')))
    else:
        print("NOT_FOUND")