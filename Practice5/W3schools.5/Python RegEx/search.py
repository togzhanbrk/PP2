import re
s = "price 1200 тг, then 900 тг"
m = re.search(r"\d+", s)
print(m.group(), m.start(), m.end())