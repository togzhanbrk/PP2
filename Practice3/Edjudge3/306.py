class Shape:
    def area():
        return 0
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    def area(self):
        return self.width * self.length

l, w = map(int, input().split())

rc = Rectangle(l, w)
print(rc.area())


