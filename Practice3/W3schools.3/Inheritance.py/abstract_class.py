from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass  # child must implement

class Dog(Animal):
    def speak(self):
        print("Woof!")

d = Dog()
d.speak()  # Woof!
