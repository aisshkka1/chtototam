import re

s = input()

res = re.match('Hello', s)
if res:
    print("Yes")
else:
    print("No")
