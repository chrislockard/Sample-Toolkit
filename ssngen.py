#!/usr/bin/python
'''
Generate pseudo-random SSNs and save to a text file.
'''
import random

try:
    myfile = open(str(raw_input("Output filename: ")), "w")
except ValueError:
    print "Invalid input.  Please enter a valid filename."

try:
    for i in range(int(raw_input("How many random numbers?: "))):
        line = str(random.randint(100000000, 999999999))
        myfile.write(line)
        myfile.write('\n')
except ValueError:
    print "User entered invalid input.  Please only enter integers."

myfile.close()
