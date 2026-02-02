n = int(input())
num = list(map(int, input().split()))
for i in range(n):
    num[i] = num[i]**2

print(*num)

