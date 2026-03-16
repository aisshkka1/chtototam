n = int(input())

a = input().split()
b = input().split()

d = dict(zip(a, b))

qu = input()

if qu in d:
    print(d[qu])
else:
    print("Not found")

