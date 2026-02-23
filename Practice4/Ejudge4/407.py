class Reverse:
    def __init__(self, text):
        self.text = text
        self.index = len(text) - 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.index < 0:
            raise StopIteration
        ch = self.text[self.index]
        self.index -= 1
        return ch
    
s = input().strip()

rev = Reverse(s)

for ch in rev:
    print(ch, end = "")
print()
