def func(s):
    yield s[::-1]

a = input()
for i in func(a):
    print(i)

