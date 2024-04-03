# Autograder for CS3500 at University of Central Missouri
# Fall 2023
# Dr. Mark Grebe
# grebe@ucmo.educa

from pathlib import Path
import os
import re
import shutil
import signal
import subprocess
import zipfile

FILEDIR = "./files/"
ZIPDIR = "./zips/"
NONBLACKDIR = "./nonblackboard/"
PROGFILE = 'progs.txt'
ZIP_EXTRACT_LIST = ['c', 'C', 'h', 'H']
PROGTIMEOUT = 2

# Remove old output directories
if os.path.exists(FILEDIR):
    shutil.rmtree(FILEDIR)
if os.path.exists(ZIPDIR):
    shutil.rmtree(ZIPDIR)

# Create new output directories
os.mkdir(FILEDIR)
os.mkdir(ZIPDIR)

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
    # Remove version number 
    new_no_ver_name = re.sub(r' \([0-9]\)','',new_name)
    os.rename(ZIPDIR + file.name, ZIPDIR + new_no_ver_name)

# Copy any zips that were submitted outside Blackboard
if os.path.exists(NONBLACKDIR):
    nonblackdir = Path(NONBLACKDIR)
    for file in nonblackdir.glob('*.zip'):
        os.system("cp " + NONBLACKDIR + "/" + file.name + " " + ZIPDIR)

# For each of the assignment zip files...
for file in zipdir.glob('*.zip'):
    # Unzip the assignment into Student dir inside the files directory
    # os.system("unzip -d " + FILEDIR + file.stem + " " + ZIPDIR + file.name)
    with zipfile.ZipFile(file) as zip:
        for zip_info in zip.infolist():
            if zip_info.is_dir():
                continue
            extension = zip_info.filename.split(".")[-1]
            if extension not in ZIP_EXTRACT_LIST :
                continue
            zip_info.filename = os.path.basename(zip_info.filename)
            zip.extract(zip_info, FILEDIR + file.stem)

    # Compile every C file in the assignment directory
    student_dir = FILEDIR + file.stem
    student_path = Path(student_dir)
    homework_path = Path('.')
    # For each of the programs in the assignment
    for prog in prog_array:
        # Compile the program
        os.system("clang -o " + student_dir + "/" + prog + " " + 
                  student_dir + "/" + prog + ".c" + 
                  " 2> " + student_dir + "/" + prog + ".compile")
        # If the program has input run it with input file and save the output
        if os.path.isfile(prog + ".input"):
            inputnum = 0
            for inputfile in homework_path.glob(prog + '.input*'):
                myinput = open(inputfile.name)
                myoutput = open(student_dir + "/" + prog + ".output" + str(inputnum), 'w')
                if os.path.isfile(student_dir + "/" + prog):
                    inputstart = prog + '.input'
                    argspath = prog + ".args" + inputfile.name[len(inputstart):]
                    if os.path.isfile(argspath):
                        with open(argspath) as my_file:
                            arglines = my_file.readlines()
                            args = arglines[0].strip().split()
                    else:
                        args = []
                    p = subprocess.Popen([student_dir + "/" + prog] + args, stdin=myinput, stdout=myoutput)
                    try:
                        p.wait(PROGTIMEOUT)
                    except:
                        myoutput.write("****** Process Timeout: " + prog + "\n")
                        p.terminate()
                    myoutput.write("****** Above output generated \n")
                    myoutput.write("****** with Test Arguments: " + arglines[0] + "\n")
                else:
                    myoutput.write("****** Executable Not Found: " + prog + "\n")
                myoutput.flush()
                myinput.close()
                myoutput.close()
                inputnum = inputnum + 1
        # Otherise just run it and save the output
        else:
            myoutput = open(student_dir + "/" + prog + ".output", 'w')
            if os.path.isfile(student_dir + "/" + prog):
                p = subprocess.Popen(student_dir + "/" + prog, stdout=myoutput)
                try:
                    p.wait(PROGTIMEOUT)
                except:
                    myoutput.write("****** Process Timeout: " + prog + "\n")
                    p.terminate()
            else:
                myoutput.write("****** Executable Not Found: " + prog + "\n")
            myoutput.flush()
            myoutput.close()
           
