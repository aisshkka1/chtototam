import re

s = input()
p = r"(\S+)@(\S+)\.(\S+)"

res = re.search(p, s)
if res:
    print(res.group())
else:
    print("No email")