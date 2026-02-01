n = int(input())
numbers = list(map(int, input().split()))

max = numbers[0]
for num in numbers:
    if num > max:
        max = num
print(max)