from pathlib import Path
import shutil

base_dir = Path("practice6_workspace")
source_file = base_dir / "sample.txt"
backup_dir = base_dir / "backup"
backup_dir.mkdir(parents=True, exist_ok=True)
backup_file = backup_dir / "sample_backup.txt"
copy_file = base_dir / "sample_copy.txt"

if not source_file.exists():
    print("Source file does not exist. Run write_files.py first.")
else:
    # Copying file to another file in the same folder
    shutil.copy(source_file, copy_file)
    print("Copied to:", copy_file)

    # Backup copy in backup folder
    shutil.copy2(source_file, backup_file)
    print("Backup created at:", backup_file)

    # Safe delete example
    if copy_file.exists():
        copy_file.unlink()
        print("Deleted:", copy_file)
    else:
        print("Nothing to delete.")
