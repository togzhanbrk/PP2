import re
s = "apples 120, bananas 90, milk 350"
print(re.findall(r"\d+", s))