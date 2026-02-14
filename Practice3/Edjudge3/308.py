class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient Funds"
        self.balance -= amount
        return self.balance

b, w = map(int, input().split())

account = Account("Toghan", b)
result = account.withdraw(w)
print(result)
