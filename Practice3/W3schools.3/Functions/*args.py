def my_function(greeting, *names): # *args → many unnamed values → tuple
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")