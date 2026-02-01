n = int(input())
strings = []

for i in range(0, n):
    s = input().strip()
    strings.append(s)

first_index = {}
for i, s in enumerate(strings):
    if s not in first_index:
        first_index[s] = i + 1

for s in sorted(first_index):
    print(s, first_index[s])
