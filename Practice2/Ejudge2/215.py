n = int(input())

names = []

for _ in range(n):
    name = input()
    names.append(name)

names.sort()
count = 0

for i in range(0, n):
    if names[i - 1] == names[i]:
        continue
    else:
        count += 1
        
if count == 0:
    count = 1
print(count)