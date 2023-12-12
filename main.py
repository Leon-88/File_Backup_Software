import time
import os
import shutil
from pathlib import Path
from datetime import datetime


def printRed(input):
    print("\033[91m {}\033[00m".format(input))


def printGreen(input):
    print("\033[92m {}\033[00m".format(input))


def printYellow(input):
    print("\033[93m {}\033[00m".format(input))


def get_size_of_directory(dir):
    size = 0
    directory = Path(dir)

    # https://docs.python.org/3/library/pathlib.html#pathlib.Path.rglob
    for item in directory.rglob("*"):
        if item.is_file():
            size += item.stat().st_size

    return size


def get_size_of_directory_MB(dir):
    # 1 MB = 1024^2 (1,048,576) Bytes (in binary)
    return round(get_size_of_directory(dir) / (1024 * 1024), 2)


# ---------------------------- main program begins --------------------------------------

# Get the current date and time for the backup folder name
date = datetime.now().strftime(r"%Y-%m-%d_%H-%M")


# Replace paths with the directory that you want to back up. You may want to use Path.home().

source_directory = Path() / "/path" / "to" / "file_you_want_to_backup"

destination_directory = Path() / "/path" / "to" / "dir_where_backups_are_saved" / date

# debug statements
# print(str(source_directory) + "\n")
# print(str(destination_directory) + "\n")

print()

try:
    if not os.path.exists(source_directory):
        raise Exception("The source directory does not exist.")

    if os.path.exists(destination_directory):
        raise Exception(
            "The destination directory already exists. Please wait at least one minute between backups."
        )

    # Copy all files and folders
    shutil.copytree(source_directory, destination_directory)
    backup_size = get_size_of_directory_MB(destination_directory)

    printGreen("Backup successful.")
    print("\tsize: ≈ " + str(backup_size) + " MB\n")

    # Count down from 5 before exiting
    for i in range(5, 0, -1):
        print("Exiting in {} second(s)...".format(i), end="\r")
        time.sleep(1)

# Wait for user input before exiting because the files have not been backed up
except Exception as e:
    printRed("Error: " + str(e))
    printRed("Files have NOT been backed up.")
    input("\nPress Enter to exit...")
