import json

x = {
    "name": "Togzhan",
    "age": 19,
    "city": "Almaty"
}

y = json.dumps(x)

print(y)