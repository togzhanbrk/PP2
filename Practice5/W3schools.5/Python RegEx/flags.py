import re

txt1 = "Eland"
print(re.findall("\w", txt1, re.ASCII))  # ascii find all ASCII matches 
print(re.findall("\w", txt1))   # without the flag, the example would return all character
print(re.findall("\w", txt1, re.A))  # same result using the shorthand re.A flag

txt2 = "The rain in Sapain"
print(re.findall("spain", txt2, re.DEBUG))  # debug Use a case-insensitive search when 
                                            #finding a match for Spain in the text
                                            # returns debug information

txt3 = """Hi
my
name
is
Sally"""
print(re.findall("me.is", txt3, re.DOTALL))  # dotall Makes the . character match all characters (including newline character)
print(re.findall("me.is", txt3))
print(re.findall("me.is", txt3, re.S))

txt4 = "The rain in Spain"
print(re.findall("spain", txt4, re.IGNORECASE)) # ignorecase Case-insensitive matching
print(re.findall("spain", txt4, re.I))

txt5 =  """There
aint much
rain in 
Spain"""
print(re.findall("^ain", txt5, re.MULTILINE)) # multiline Returns only matches at the beginning of each line
print(re.findall("^ain", txt5))
print(re.findall("^ain", txt5, re.M))

txt6 = "Eland"
print(re.findall("\w", txt6, re.UNICODE))  # Returns Unicode matches. This is default from Python 3. 
                                           # For Python 2: use this flag to return only Unicode matches
print(re.findall("\w", txt6, re.U))


text = "The rain in Spain falls mainly on the plain"  # Allows whitespaces and comments inside patterns. 
                                                      # Makes the pattern more readable
pattern = """
[A-Za-z]* #starts with any letter
ain+      #contains 'ain'
[a-z]*    #followed by any small letter
"""
print(re.findall(pattern, text, re.VERBOSE))
print(re.findall(pattern, text))
print(re.findall(pattern, text, re.X))
