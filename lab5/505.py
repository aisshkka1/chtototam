import re

s = input()
p = "^([A-Za-z']+)([0-9])$"

res = re.findall(p, s)
if res:
    print("Yes")
else:
    print("No")
