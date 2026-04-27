def func(n):
    for i in range(n+1):
        yield int(2**i)

a = int(input())
for i in func(a):
    print(i, end = " ")     
