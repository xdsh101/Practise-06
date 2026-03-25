from pathlib import Path
import shutil

base_dir = Path("move_demo")
source_dir = base_dir / "source"
destination_dir = base_dir / "destination"
backup_dir = base_dir / "backup"

source_dir.mkdir(parents=True, exist_ok=True)
destination_dir.mkdir(parents=True, exist_ok=True)
backup_dir.mkdir(parents=True, exist_ok=True)

source_file = source_dir / "data.txt"
source_file.write_text("This file will be copied and moved.\n", encoding="utf-8")

# Copy file to backup directory
shutil.copy2(source_file, backup_dir / source_file.name)
print("Copied to backup folder.")

# Move file to destination directory
moved_file = shutil.move(str(source_file), destination_dir / source_file.name)
print("Moved file to:", moved_file)

print("\nFiles in destination:")
for file in destination_dir.iterdir():
    print(file.name)
