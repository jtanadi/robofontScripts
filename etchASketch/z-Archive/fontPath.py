thisFont = CurrentFont()

def fileInfo():
        fullPath = thisFont.path
        fileName = thisFont.fileName
        #fileName = thisFont.path.split('/')[-1]
        #filePath = fullPath.rstrip(fileName)
        #return fullPath, filePath, a
        return fileName
        
#print fileInfo()

fileInfo = fileInfo()

print fileInfo[0]
print fileInfo[1]
#print fileInfo[2]