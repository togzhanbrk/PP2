n = int(input())

numbers = list(map(int, input().split()))

freq = {}

for x in numbers:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_freq = 0
answer = None

for x in freq:
    if freq[x] > max_freq:
        max_freq = freq[x]
        answer = x
    elif freq[x] == max_freq and x < answer:
        answer = x

print(answer)

