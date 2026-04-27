def func(a, k):
    for i in range(k):
        for j in a:
            yield j

a = input().split()
b = int(input())
for i in func(a, b):
    print(i, end = " ") 
