import re

s = input()
p = r"\b[A-Za-z']{3}\b"

res = re.findall(p, s)
print(len(res))