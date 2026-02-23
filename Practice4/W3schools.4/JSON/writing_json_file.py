import json

data = {
    "name": "Ali",
    "age": 20
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
