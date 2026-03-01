import re
s = "Card: 5555 6666 7777 8888"
print(re.sub(r"\d", "X", s))