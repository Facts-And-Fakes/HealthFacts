# Importing libraries
import time
import os


def open_program():
    # ask user for time interval and program
    timeint = -1
    program = ""
    while timeint == -1:
        try:
            timeint = float(input("Enter time interval: "))
        except ValueError:
            print("Please enter a number")
            timeint = float(input("Enter time interval: "))
    while program == "":
        program = input("Which program to open? (Ensure the spelling is correct - Eg. Notepad): ")

    # countdown
    print("Three")
    time.sleep(1)
    print("Two")
    time.sleep(1)
    print("One")
    time.sleep(1)
    print("GO!")

    # sleep
    time.sleep(timeint)

    # open required program
    try:
        os.system(program)
    except:
        print("Could not open program.")


open_program()
