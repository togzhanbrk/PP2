def limited_cycle(n, k):
    for i in range(k):
        yield n

n = list(map(str, input().split()))
k = int(input())

for elem in limited_cycle(n, k):
    print(*elem, end = " ")