# reduce() combines all elements into one result

from functools import reduce

numbers = [1, 2, 3, 4, 5]

sum_all = reduce(lambda x, y: x + y, numbers)

print(sum_all)

# Example for multiplication:

nums = [3, 6, 7, 8]

product = reduce(lambda x, y: x * y, nums)

print(product)