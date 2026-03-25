from pathlib import Path

file_path = Path("practice6_workspace") / "sample.txt"

if not file_path.exists():
    print("File does not exist. Run write_files.py first.")
else:
    # Read the whole file
    with open(file_path, "r", encoding="utf-8") as file:
        all_text = file.read()
    print("Using read():")
    print(all_text)

    # Read one line at a time
    with open(file_path, "r", encoding="utf-8") as file:
        print("Using readline():")
        print(file.readline().strip())
        print(file.readline().strip())

    # Read all lines into a list
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    print("Using readlines():")
    for line in lines:
        print(line.strip())