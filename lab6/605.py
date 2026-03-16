n = input()
vowel = "aeiouAEIOU"

if any(ch in vowel for ch in n):
    print("Yes")
else:
    print("No")