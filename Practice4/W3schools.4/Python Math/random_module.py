import random

print(random.random()) #between 0 and 1

print(random.randint(1, 40))

colors = ["red", "green", "brown"]
print(random.choice(colors))

nums = [1, 2, 3, 4, 5, 6]
random.shuffle(nums)

print(nums)