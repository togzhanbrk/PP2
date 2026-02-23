def prime_num(n):
    for num in range(2, n + 1):
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                break
        else:
            yield num

n = int(input())

for num in prime_num(n):
    print(num, end = " ")

print()
    