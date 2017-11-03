import re

f = CurrentFont()

glyphNameList = [g.name for g in f]
    
ucMatchList = []
lcMatchList = []

for index, item in enumerate(glyphNameList):
    
    lcMatch = re.match(r"(\b[a-z](.(ss[\d]+|alt([\d]?)+))?\b)|dotlessi", glyphNameList[index]) #regex will include .ss and .alt variations
    
    ucMatch = re.match(r"\b[A-Z](.(ss[\d]+|alt([\d]?)+))?\b", glyphNameList[index]) #regex will include .ss and .alt variations
    
    if lcMatch:
        lcMatchList.append(lcMatch.group())

    elif ucMatch:
        ucMatchList.append(ucMatch.group())

print "upper case list"
print sorted(ucMatchList)

print "\n lower case list"
print sorted(lcMatchList)