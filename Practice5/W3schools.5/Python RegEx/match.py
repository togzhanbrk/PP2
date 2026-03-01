import re
print(bool(re.match(r"\d+", "123abc")))
print(bool(re.match(r"\d+", "abc123")))