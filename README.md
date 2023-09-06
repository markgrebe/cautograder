# Autograder for UCM CS3500 Fall 2023

Files for each homework are stored in subdirectories named HW?? (where ?? is Homwork number)
They include:
    progs.txt - A text file containing one line for each expected program name.
    {programname}.input - A text file containging the test data for that program.

The downloaded gradebook*.zip from Blackboard should be copied into the HW?? directory before running the autograder.

Any student assignments zip files received outside of blackboard may be placed in the HW??/nonblackboard directory before running the autograder.

Autograder is ran from the command line in the HW?? directory with the following command:
```
python3 ../autograder.py
```

The autograder will create a HW??/files directory containing a subdirectory for each of the students.

The HW??/files/{student70000000} directories will contain any .c and .h files found in the student zip that was submitted.

The autograder will attempt to compile and run the .c's corresponding to the program names in HW??/progs.txt.

It will create a {progname}.compile containing any errors or warnings from the compilation, and a {progname}.output with the text output from the running of the student program.

