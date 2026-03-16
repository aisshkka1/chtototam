n = int(input())
words = input().split()
iwords = []
for i, word in enumerate(words):
    iwords.append(f"{i}:{word}")
print(" ".join(iwords))

