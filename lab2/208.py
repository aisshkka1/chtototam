n = int(input())

for i in range(0, 31):
    if 2 ** i <= n:
        print(2 ** i, end=" ")
    else:
        break