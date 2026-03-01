import re

txt = "The rain in Spain"

x = re.findall("\AThe", txt)  # Returns a match if the specified 
print(x)                      # characters are at the beginning of the string
if x:
  print("Yes, there is a match!")
else:
  print("No match")


txt = "The rain in Spain"       # Returns a match where the specified characters are 
x = re.findall(r"\bain", txt)   # at the beginning or at the end of a word
print(x)
if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

  
