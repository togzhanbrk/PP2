n = int(input())

sequence = list(map(int, input().split()))

max_value = max(sequence)

position = sequence.index(max_value) + 1

print(position)

