import json

with open("/Users/togzhan/vscode/PP2/Practice4/W3schools.4/JSON/sample-data.json", "r") as f:
    data = json.load(f)

for student in data["students"]:
    print(student["name"], student["grade"])

total = 0

for student in data["students"]:
    total += student["grade"]

avg = total / len(data["students"])
print(avg)

