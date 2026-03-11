a = int(input())

nums = map(int, input().split())

squares = list(map(lambda x: x**2, nums))

sum = 0
for s in squares:
    sum += s

print(sum)