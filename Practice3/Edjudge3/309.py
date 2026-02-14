class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        pi = 3.14159
        print(f"{(self.radius ** 2 * pi):.2f}")

r = int(input())
circle = Circle(r)
circle.area()