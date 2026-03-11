n = int(input())

numbers = map(int, input().split())

even_nums = list(filter(lambda x: x % 2 == 0, numbers))

count = 0
for num in even_nums:
    count += 1

print(count)