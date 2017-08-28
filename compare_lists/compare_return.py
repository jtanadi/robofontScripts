"""
--------------------------------------------------------
--------------------------------------------------------
 Compare 2 return-separated lists (e.g., list of files)
--------------------------------------------------------
--------------------------------------------------------

This script compares 2 return-separated lists from 2 text files and
writes the "difference" to a third text file (currently named "difference.txt").

Prior to running the script, remember to change paths & file names.
difference.txt will be created if no such file exists.
"""

import sys

with open(raw_input("First file: "), 'rU') as file1: #Prompts user to type in file name
    charSet1 = file1.readlines() #Returns a list

with open(raw_input("Second file: "), 'rU') as file2: #Prompts user to type in file name
    charSet2 = file2.readlines() #Returns a list

#Writes result to file (new if file doesn't exist)
sys.stdout = open('/Users/jesentanadi/Desktop/difference.txt', 'w+')

#Removes extra line breaks and inserts list back into the same variable ("list comprehension")
charSet1 = [item.replace("\n", "") for item in charSet1] 
charSet2 = [item.replace("\n", "") for item in charSet2]

#Goes through 1st list & compares with 2nd list
print "In 1st char set:"
for char in charSet1:
	if char not in charSet2:
		print char

#Goes through 2nd list & compares with 1st list
print "\nIn 2nd char set:" 
for char in charSet2:
	if char not in charSet1:
		print char

"""
---------------
     TO DO
---------------

+ "Open File" window to choose text files
+ Combine with space-separated script

"""
