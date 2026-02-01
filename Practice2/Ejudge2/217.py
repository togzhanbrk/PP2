n = int(input())

phone_numbers = []

for i in range(0, n):
    x = input().strip()
    phone_numbers.append(x)

freq = {}
for x in phone_numbers:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1
 
count = 0
for x in freq:
    if freq[x] == 3:
        count += 1

print(count)


