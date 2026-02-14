class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    def speak(self):  # override
        print("Woof!")

a = Animal()
a.speak()  # Some sound

d = Dog()
d.speak()  # Woof! (overridden)
