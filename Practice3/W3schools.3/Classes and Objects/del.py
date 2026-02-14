class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def myfunc(self):
        print("Hello my name is " + self.name)
    
p1 = Person("Togzhan", 19)
del p1
p1.myfunc()