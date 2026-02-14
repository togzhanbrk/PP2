def valid_num(number):
    valid = True
    for n in str(number):
        if int(n) % 2 != 0:
            return False
    return True

number = int(input())
if valid_num(number):
    print("Valid")
else:
    print("Not valid")
            

            
