s = input()

num= []

for ch in s:
    if ch.isdigit():
        num.append(ch)

print(" ".join(num))