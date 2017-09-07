from robofab.interface.all.dialogs import Message
from vanilla import *
import re

f = CurrentFont()

selectedGlyphs = [f[glyph] for glyph in f.selection]
glyphName = [glyph.name for glyph in f]

ucList = []
lcList = []
sourceList = []
       
class CopySideBearings(object):

    def __init__(self):
        self.upperCase = 0
        self.lowerCase = 0
        
        self.generateRegexList()
                  
        self.buildUI()
        self.w.open()


    def buildUI(self):
        
        self.w = FloatingWindow((1000, 400, 200, 200),
                 "Copy SB")
        
        self.w.textTarget = TextBox((10, 10, -10, 20),
                            "Target")
        self.w.radioTarget = RadioGroup((25, 33, 150, 20),
                             ["Left SB", "Right SB"],
                             isVertical = False,
                             callback=self.radioTargetCallback)

        self.w.line = HorizontalLine((10, 61, -10, 1))
        
        self.w.textSource = TextBox((10, 70, -10, 20),
                            "Source")                            
        self.w.radioSource = RadioGroup((25, 93, 150, 20),
                             ["Left SB", "Right SB"],
                             isVertical = False,
                             callback=self.radioSourceCallback)
        
        self.w.checkboxUC = CheckBox((10, 125, 45, 20),
                            "UC",
                            callback=self.checkboxUCcallback)      
        self.w.checkboxLC = CheckBox((55, 125, 50, 20),
                            "LC",
                            callback=self.checkboxLCcallback)
        self.w.sourceGlyphBox = ComboBox((105, 125, 85, 21),
                                sourceList,
                                callback=self.sourceGlyphBoxCallback,
                                completes=False,
                                continuous=True)
       
        self.w.okButton = Button((10, 159, -10, 20),
                        "OK",
                        callback=self.okButtonCallback)
        

    def generateRegexList(self):
    
        for index, item in enumerate(glyphName):
    
            lcMatch = re.match(r"(\b[a-z](.(ss[\d]+|alt([\d]?)+))?\b)|dotlessi", glyphName[index]) #regex will include .ss and .alt variations
    
            ucMatch = re.match(r"\b[A-Z](.(ss[\d]+|alt([\d]?)+))?\b", glyphName[index]) #regex will include .ss and .alt variations
    
            if lcMatch:
                lcList.append(lcMatch.group())
                
            elif ucMatch:
                ucList.append(ucMatch.group())
                
                
    def radioTargetCallback(self, sender):

        self.targetIndex = sender.get()

        
    def radioSourceCallback(self, sender):

        self.sourceIndex = sender.get()

    
    def checkboxUCcallback(self, sender):
        
        self.upperCase = sender.get()
        
        self.checkCase()

    
    def checkboxLCcallback(self, sender):
    
        self.lowerCase = sender.get()
        
        self.checkCase()
    
    
    def sourceGlyphBoxCallback(self, sender):
        
       self.gSource = f[sender.get()]


    def checkCase(self):

        if self.upperCase == 1 and self.lowerCase == 1:
            self.sourceList = sorted(ucList + lcList)
            self.w.sourceGlyphBox.setItems(self.sourceList)
            
        elif self.upperCase == 1 and self.lowerCase == 0:
            self.sourceList = sorted(ucList)
            self.w.sourceGlyphBox.setItems(self.sourceList)
            
        elif self.upperCase == 0 and self.lowerCase == 1:
            self.sourceList = sorted(lcList)
            self.w.sourceGlyphBox.setItems(self.sourceList)
        
        elif self.upperCase == 0 and self.lowerCase == 0:
            self.sourceList = []
            self.w.sourceGlyphBox.setItems(self.sourceList)
            
                             
    def okButtonCallback(self, sender):
        
        self.computeSidebearings()
        self.w.close()


    def computeSidebearings(self):
        
        sourceLeft = int(self.gSource.leftMargin)
        sourceRight = int(self.gSource.rightMargin)
        
        if self.targetIndex == 0:
            if self.sourceIndex == 0:
                for gTarget in selectedGlyphs:
                    gTarget.leftMargin = sourceLeft
            
            elif self.sourceIndex == 1:
                for gTarget in selectedGlyphs:
                    gTarget.leftMargin = sourceRight
        
        elif self.targetIndex == 1:
            if self.sourceIndex == 0:
                for gTarget in selectedGlyphs:
                    gTarget.rightMargin = sourceLeft
            
            elif self.sourceIndex == 1:
                for gTarget in selectedGlyphs:
                    gTarget.rightMargin = sourceRight

        
CopySideBearings()

"""
---------------
     TO DO
---------------
+ BUG: Weird combo box bug that repeats characters that proceed the first (e.g. typing "de" yields "dee," "deg" yields "deegg")
+ BUG: Invalid glyphs also get doubled (anything not in UC & lc)

+ Add alerts for empty or invalid source glyph entries

"""
