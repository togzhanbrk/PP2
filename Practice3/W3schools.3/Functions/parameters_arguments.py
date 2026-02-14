def my_function(name):  # name is a parameter
    print("Hello", name)

my_function("Togzhan")  # "Togzhan" is an argument

#positional-only arguments
def arg_function(name, /):
    print("Hello", name)
arg_function("Togzhan") #works, if we write code like that arg_function(name = 'Togzhan') we will have error

#keyword-only arguments
def key_function(*, name):
    print("Hello", name)
key_function(name = "Togzhan") #works, if we write code like that key_function("Togzhan") we will habe error