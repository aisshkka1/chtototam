a = int(input())
b = list(map(int, input().split()))

if all( n >= 0 for n in b):
    print("Yes")
else:
    print("No")
