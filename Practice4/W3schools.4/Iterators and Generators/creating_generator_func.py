def name_of_peple():
    yield "Togzhan"
    yield "Tom"
    yield "Linus"

name = name_of_peple()

print(next(name))
print(next(name))
print(next(name))