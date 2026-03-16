n = int(input())
num = list(map(int, input().split()))
summ = 0
for i in num:
    summ += i*i
print(summ)
