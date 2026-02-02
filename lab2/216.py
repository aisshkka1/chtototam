a = int(input())
num = list(map(int, input().split()))
seen = []
for i in range(a):
    if num[i] not in seen:
        print("YES")
        seen.append(num[i])
    else:
        print("NO")