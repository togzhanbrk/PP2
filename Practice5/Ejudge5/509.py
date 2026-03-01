import re

text = input()

words = re.findall(r"\b[a-zA-Z]{3}\b", text)

print(len(words))
