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

    student_dir = FILEDIR + file.stem
    student_path = Path(student_dir)
    homework_path = Path('.')
    # Compile the program
    os.system("clang -o " + student_dir + "/chess " + 
              student_dir + "/chess.c " + 
              student_dir + "/square.c" + 
              " 2> " + student_dir + "/chess.compile")
    myoutput = open(student_dir + "/chess.output", 'w')
    if os.path.isfile(student_dir + "/chess"):
        p = subprocess.Popen(student_dir + "/chess", stdout=myoutput)
        try:
            p.wait(PROGTIMEOUT)
        except:
            myoutput.write("****** Process Timeout: chess\n")
            p.terminate()
    else:
        myoutput.write("****** Executable Not Found: chess\n")
    myoutput.flush()
    myoutput.close()
       
