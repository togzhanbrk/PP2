n = int(input())
numbers = list(map(int, input().split()))

max = numbers[0]
min = numbers[0]

for num in numbers:
    if num > max:
        max = num
    elif num < min:
        min = num

for num in numbers:
    if num == max:
        num = min
    print(num, end = " ")