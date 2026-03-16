n = int(input())
num = list(map(int, input().split()))

def func(x):
    return x % 2 ==0

even_numbers = filter(func, num)
print(len(list(even_numbers)))
