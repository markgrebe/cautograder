#!/Users/markg/.pyenv/shims/python
from pathlib import Path
import os

ZIPDIR = "./zips/"
FILEDIR = "./files/"
PROGFILE = 'progs.txt'

# Get the list of program names from grade.txt
prog_array = []
with open(PROGFILE) as my_file:
    for line in my_file:
        prog_array.append(line[:-1])

# Unzip the Blackboard Assignment archive and unzip it into the zips directory
os.system("unzip -d zips/ gradebook*.zip")

# Rename all of the assignment zips, leaving just lastname700.zip
zipdir = Path(ZIPDIR)
for file in zipdir.glob('*.zip'):
    new_name = file.name.split('_')[-1]
    os.rename(ZIPDIR + file.name, ZIPDIR + new_name)

# For each of the assignment zip files...
for file in zipdir.glob('*.zip'):
    # Unzip the assignment into Student dir inside the files directory
    os.system("unzip -d " + FILEDIR + file.stem + " " + ZIPDIR + file.name)

    # Compile every C file in the assignment directory
    student_dir = FILEDIR + file.stem
    student_path = Path(student_dir)
    #for cfile in student_path.glob('*.c'):
    for prog in prog_array:
        os.system("clang -o " + student_dir + "/" + prog + " " + 
                  student_dir + "/" + prog + ".c" + 
                  " 2> " + student_dir + "/" + prog + ".compile")
        if os.path.isfile(prog + ".input"):
            os.system(student_dir + "/" + prog + 
                      " < ./" + prog + ".input" +
                      " > " + student_dir + "/" + prog + ".run")
        else:
             os.system(student_dir + "/" + prog + 
                      " > " + student_dir + "/" + prog + ".run")
           


