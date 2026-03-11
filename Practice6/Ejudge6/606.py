n = int(input())

numbers = map(int, input().split())

result = all(num >= 0 for num in numbers)

if result:
    print("Yes")
else:
    print("No")