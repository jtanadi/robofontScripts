f = CurrentFont()

class LearnStuff():
    def getFontMetrics(self):
        return f.info.xHeight, f.info.ascender, f.info.descender
        
        
    def getFontName(self):
        return f.info.familyName, f.info.styleName
        
    def getFileInfo(self):
        name = f.path.split("/")[-1]
        
        return name, f.path.rstrip(name)

info = LearnStuff()

print info.getFontMetrics()
print info.getFontName()
print info.getFileInfo()