class Mother:
    def skills(self):
        print("Cooking")

class Father:
    def skills(self):
        print("Driving")

class Child(Mother, Father):
    pass

c = Child()
c.skills()  # Cooking → Python MRO (Method Resolution Order) using first class skill
