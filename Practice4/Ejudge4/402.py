n = int(input())

def even_num(n):
    for x in range(0, n + 1, 2):
        yield x

first = True
for x in even_num(n):
    if first:
        print(x, end= "")
        first = False
    else:
        print("," + str(x), end = "")

print()