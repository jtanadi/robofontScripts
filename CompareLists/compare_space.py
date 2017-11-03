"""
--------------------------------------------------------
--------------------------------------------------------
 Compare 2 space-separated lists (e.g., character sets)
--------------------------------------------------------
--------------------------------------------------------

This script compares 2 space-separated lists from 2 text files and
writes the "difference" to a third text file (currently named "difference.txt").

Prior to running the script, remember to change paths & file names.
difference.txt will be created if no such file exists.
"""

import sys

with open(raw_input("First file: "), 'r') as file1: #Prompts user to type in file name
    charSet1 = file1.read() #Returns 1 big string

with open(raw_input("Second file: "), 'r') as file2: #Prompts user to type in file name
    charSet2 = file2.read() #Returns 1 big string

#Writes result to file (new if file doesn't exist)
sys.stdout = open('/Users/jesentanadi/Desktop/difference.txt', 'w+')

#Splits the string into a list of strings using whitespace. For comma-separated lists, use .splid(",")
charSet1 = charSet1.split() 
charSet2 = charSet2.split()

#Goes through 1st list & compares with 2nd list
print "In 1st char set:"
for char in charSet1:
	if char not in charSet2:
		print char,

#Goes through 2nd list & compares with 1st list
print "\n\nIn 2nd char set:"
for char in charSet2:
	if char not in charSet1:
		print char,

"""
---------------
     TO DO
---------------

+ "Open File" window to choose text files
+ Combine with space-separated script

"""
