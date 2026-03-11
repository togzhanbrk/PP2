n = int(input())

n_keys = list(input().split())
n_values = list(input().split())

char = input()

found = False

for key, value in zip(n_keys, n_values):
    if key == char:
        print(value)
        found = True
        break

if not found:
    print("Not found")