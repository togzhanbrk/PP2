n = int(input())

numbers = list(map(int, input().split()))

for num in numbers:
    print(num * num, end = " ")