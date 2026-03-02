import re

s = input()
p = input()

res = re.findall(p, s)
print(len(res))