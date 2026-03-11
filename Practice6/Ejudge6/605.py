string = input()

vowels = ["a", "e", "i", "o", "u"]

result = any(s in vowels for s in string.lower())

if result:
    print("Yes")
else:
    print("No")

