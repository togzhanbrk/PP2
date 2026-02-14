numbers = [1, 2, 3, 4, 5]

# Regular функция
def square(x):
    return x * x
squared = list(map(square, numbers))
print(squared)  

# Lambda функция
squared = list(map(lambda x: x * x, numbers))
print(squared)  
