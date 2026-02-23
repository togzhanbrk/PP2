def power_of_two(n):
    for i in range(n + 1):
        yield 2 ** i

n = int(input())

for num in power_of_two(n):
    print(num, end=" ")