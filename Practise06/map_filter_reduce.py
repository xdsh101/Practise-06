from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
strings = ["10", "20", "30"]

# map()
squares = list(map(lambda x: x * x, numbers))
print("Squares:", squares)

# filter()
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# reduce()
total_product = reduce(lambda a, b: a * b, [1, 2, 3, 4])
print("Product using reduce:", total_product)

# Other
print("Length:", len(numbers))
print("Sum:", sum(numbers))
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))

# Type conversions
converted_ints = list(map(int, strings))
print("Converted to integers:", converted_ints)
print("Converted to float:", float("15.75"))
print("Converted to string:", str(100))
print("Converted to list:", list((1, 2, 3)))

# Type checking
print("Type of numbers:", type(numbers))
print("Is converted_ints a list?", isinstance(converted_ints, list))