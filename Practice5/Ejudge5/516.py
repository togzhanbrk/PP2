import re

text = input()

m = re.search("Name: \s*(.+), \s*Age:\s*(.+)", text)

if m:
    print(m.group(1), m.group(2))