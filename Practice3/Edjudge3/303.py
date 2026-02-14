triplet = {"ONE": 1, "TWO": 2, "THR": 3, "FOU": 4, "FIV": 5,
           "SIX": 6, "SEV": 7, "EIG": 8, "NIN": 9, "ZER": 0}
rev_triplet = {v : k for k, v in triplet.items()}

def triplet_to_number(s):
    n = 0
    for i in range(0, len(s), 3):
        t = s[i:i+3]
        n = n * 10 + triplet[t]
    return n

def number_to_triplet(num):
    if num == 0:
        return rev_triplet[0]
    result = ""
    for digit in str(num):
        result += rev_triplet[int(digit)]
    return result

expr = input().strip()

for op in "+-*":
    if op in expr:
        operator = op
        left, right = expr.split(op)
        break

num1 = triplet_to_number(left)
num2 = triplet_to_number(right)

if operator == '+':
    res = num1 + num2
elif operator == '-':
    res = num1 - num2
elif operator == "*":
    res = num1 * num2

output = number_to_triplet(res)
print(output)