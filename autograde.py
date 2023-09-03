#!/Users/markg/.pyenv/shims/python

from pathlib import Path
import os

# Unzip the Blackboard Assignment archive and unzip it into the zips directory
os.system("unzip -d zips/ gradebook*.zip")

# Rename all of the assignment zips, leaving just lastname700.zip
zipdir = Path("./zips/")
for file in zipdir.glob('*.zip'):
    new_name = file.name.split('_')[-1]
    os.rename("zips/" + file.name, "zips/" + new_name)

# For each of the assignment zip files...
for file in zipdir.glob('*.zip'):
    # Unzip the assignment into Student dir inside the files directory
    os.system("unzip -d files/" + file.stem + " zips/" + file.name)

    # Compile every C file in the assignment directory
    student_dir_str = "files/" + file.stem
    student_dir = Path(student_dir_str)
    for cfile in student_dir.glob('*.c'):
        os.system("clang -o " + student_dir_str + "/" + cfile.stem + " " + student_dir_str + "/" + cfile.name)
