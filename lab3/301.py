a = int(input())
b =str(a)
for i in b:
    dig = int(i)
    if dig % 2 != 0:
        print("Not valid")
        break
else:
        print("Valid")


