n = int(input())

a_nums = map(int, input().split())
b_nums = map(int, input().split())

sum = 0

for a, b in zip(a_nums, b_nums):
    product = a * b
    sum += product

print(sum)