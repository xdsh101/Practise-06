names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

print("Using enumerate():")
for index, name in enumerate(names, start=1):
    print(index, name)

print("\nUsing zip():")
for name, score in zip(names, scores):
    print(name, score)

# Combine data into pairs and sort by score
paired_data = list(zip(names, scores))
sorted_pairs = sorted(paired_data, key=lambda item: item[1], reverse=True)

print("\nSorted pairs by score:")
for name, score in sorted_pairs:
    print(name, score)
