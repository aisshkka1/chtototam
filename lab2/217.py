a = int(input())
num = []
seen = []

for _ in range(a):
    num.append(input().strip())  

cnt1 = 0

for i in num:
    if i not in seen:
        seen.append(i)

for x in seen:
    if num.count(x) == 3:  
        cnt1 += 1

print(cnt1)
