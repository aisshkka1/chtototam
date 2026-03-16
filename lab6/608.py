a = int(input())
num = list(map(int, input().split()))
 
num2 = set(num)
num3 = sorted(num2)
print(*num3)
