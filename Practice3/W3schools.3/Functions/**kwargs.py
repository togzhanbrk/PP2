def my_function(username, **details):   # **kwargs → many named values → dictionary
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print("  ", key + ":", value)

my_function("emil123", age = 25, city = "Oslo", hobby = "coding")
