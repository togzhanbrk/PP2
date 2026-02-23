def divisibility(n):
    for i in range(n + 1):
        if(i % 3 == 0 and i % 4 == 0):
            yield i

n = int(input())

for num in divisibility(n):
    print(str(num), end = " ")

print()