from pathlib import Path

# Create a workspace folder using pathlib
base_dir = Path("practice6_workspace")
base_dir.mkdir(exist_ok=True)

file_path = base_dir / "sample.txt"
exclusive_file = base_dir / "created_with_x.txt"

# w mode: create or overwrite the file
sample_lines = [
    "Alice, 111-222-3333\n",
    "Bob, 222-333-4444\n",
    "Charlie, 333-444-5555\n",
]

with open(file_path, "w", encoding="utf-8") as file:
    file.writelines(sample_lines)

print("Created and wrote to:", file_path)

# a mode: append new lines
with open(file_path, "a", encoding="utf-8") as file:
    file.write("David, 444-555-6666\n")
    file.write("Eva, 555-666-7777\n")

print("Appended new lines to:", file_path)

# x mode: create a new file only if it does not already exist
if not exclusive_file.exists():
    with open(exclusive_file, "x", encoding="utf-8") as file:
        file.write("This file was created using x mode.\n")
    print("Created with x mode:", exclusive_file)
else:
    print("x mode file already exists:", exclusive_file)

# Verify final content
with open(file_path, "r", encoding="utf-8") as file:
    print("\nFinal file content:")
    print(file.read())