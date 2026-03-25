from pathlib import Path
import os

base_dir = Path("directory_demo")

# os.mkdir() creates a single directory
if not os.path.exists(base_dir):
    os.mkdir(base_dir)

# os.makedirs() creates nested directories
os.makedirs(base_dir / "documents" / "texts", exist_ok=True)
os.makedirs(base_dir / "images", exist_ok=True)
os.makedirs(base_dir / "backup", exist_ok=True)
os.makedirs(base_dir / "empty_folder", exist_ok=True)

# Sample files with pathlib
(base_dir / "documents" / "texts" / "notes.txt").write_text("Python file handling\n", encoding="utf-8")
(base_dir / "documents" / "texts" / "report.txt").write_text("Directory example\n", encoding="utf-8")
(base_dir / "images" / "photo.jpg").write_text("fake image file\n", encoding="utf-8")

print("Current working directory:", os.getcwd())
print("\nItems in directory_demo:")
for item in os.listdir(base_dir):
    print(item)

print("\nAll .txt files:")
for path in base_dir.rglob("*.txt"):
    print(path)

# Demonstrate os.chdir() and os.getcwd()
original_dir = Path.cwd()
os.chdir(base_dir)
print("\nChanged working directory to:", os.getcwd())
os.chdir(original_dir)
print("Returned to:", os.getcwd())

# Demonstrate os.rmdir() on an empty directory
empty_folder = base_dir / "empty_folder"
if empty_folder.exists():
    os.rmdir(empty_folder)
    print("\nRemoved empty directory:", empty_folder)