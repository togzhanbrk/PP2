n = int(input())

nums = map(int, input().split())

result = sorted(set(nums))

for num in result:
    print(num, end=" ")

print()