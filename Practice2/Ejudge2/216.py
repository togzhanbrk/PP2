n = int(input())

numbers = list(map(int, input().split()))

seen = set()

for x in numbers:
    if x in seen:
        print("NO")
    else:
        print("YES")
        seen.add(x)
