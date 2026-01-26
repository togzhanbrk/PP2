txt = "hello world 123"

x = txt.capitalize()
print(x)

x = txt.casefold()
print(x)

x = txt.center(20)
print(x)

x = txt.count("l")
print(x)

x = txt.encode()
print(x)

x = txt.endswith("123")
print(x)

x = txt.expandtabs(4)
print(x)

x = txt.find("world")
print(x)

x = "My name is {}".format("Togzhan")
print(x)

data = {"name": "Togzhan"}
x = "My name is {name}".format_map(data)
print(x)

x = txt.index("world")
print(x)

x = txt.isalnum()
print(x)

x = txt.isalpha()
print(x)

x = txt.isascii()
print(x)

txt2 = "123"
x = txt2.isdecimal()
print(x)

x = txt2.isdigit()
print(x)

x = txt.isidentifier()
print(x)

x = txt.islower()
print(x)

x = txt2.isnumeric()
print(x)

x = txt.isprintable()
print(x)

txt3 = "   "
x = txt3.isspace()
print(x)

txt4 = "Hello World"
x = txt4.istitle()
print(x)

x = txt4.isupper()
print(x)

words = ["Hello", "World"]
x = " ".join(words)
print(x)

x = txt.ljust(20)
print(x)

x = txt.lower()
print(x)

x = txt.lstrip()
print(x)

table = str.maketrans("h", "H")
print(table)

x = txt.partition("world")
print(x)

x = txt.replace("hello", "hi")
print(x)

x = txt.rfind("l")
print(x)

x = txt.rindex("l")
print(x)

x = txt.rjust(20)
print(x)

x = txt.rpartition("world")
print(x)

x = txt.rsplit(" ")
print(x)

x = txt.rstrip()
print(x)

x = txt.split(" ")
print(x)

x = txt.splitlines()
print(x)

x = txt.startswith("hello")
print(x)

x = txt.strip()
print(x)

x = txt.swapcase()
print(x)

x = txt.title()
print(x)

x = txt.translate(table)
print(x)

x = txt.upper()
print(x)

txt5 = "42"
x = txt5.zfill(5)
print(x)

