x = int(input())
x += 1
print(x)

x -= 1
print(x)

x *= 2
print(x)

x //= 2
print(x)

x %= 3
print(x)

x //= 3
print(x)

x **= 2
print(x)

x &= 3
print(x)

x |= 3
print(x)

x ^= 2
print(x)

x >>= 3
print(x)

x <<= 3
print(x)

numbers = [1, 2, 3, 4, 5]

if(count := len(numbers)) > 3:
    print(f"List has {count} elements")