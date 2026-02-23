def fibo_gen():
    a, b = 0, 1

    while True:
        yield a
        a, b = b, a + b

n = int(input())
gen = fibo_gen()

first = True
for num in range(n):
    num = next(gen)
    if first:
        print(num, end="")
        first = False
    else:
        print("," + str(num), end="")

print()



