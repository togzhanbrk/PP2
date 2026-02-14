class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def add(self, other):
        a_sum = self.a + other.a
        b_sum = self.b + other.b
        return a_sum, b_sum
    
a1, b1, a2, b2 = map(int, input().split())
p1 = Pair(a1, b1)
p2 = Pair(a2, b2)

result = p1.add(p2)
print(f"Result: {result[0]} {result[1]}")

        