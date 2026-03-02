import re

s = input()
p = input()

res = re.split(p,  s)
print(",".join(res))