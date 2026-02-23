list_com = [x * x for x in range(5)]
print(list_com)

gen_exp = (x*x for x in range(5))
print(gen_exp)
print(list(gen_exp))

total = sum(x * x for x in range(10))
print(total)