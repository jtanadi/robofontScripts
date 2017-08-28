from robofab.interface.all.dialogs import Message
from vanilla import *
from re import *

f = CurrentFont()

gList = [f[glyph] for glyph in f.selection]
gName = sorted([g.name for g in f])
       
class SideBearing(object):

    def __init__(self):
                  
        self.buildUI()
        self.w.open()


    def buildUI(self):
        
        self.w = FloatingWindow((1000, 500, 200, 200), "Copy SB")
        self.w.textTarget = TextBox((10, 10, -10, 20), "Target")
        self.w.radioTarget = RadioGroup((25, 30, 150, 20), ["Left SB", "Right SB"], isVertical = False, callback=self.radioTargetCallback)

        self.w.line = HorizontalLine((10, 60, -10, 1))
        
        self.w.textSource = TextBox((10, 70, -10, 20), "Source")
        self.w.radioSource = RadioGroup((25, 90, 150, 20), ["Left SB", "Right SB"], isVertical = False, callback=self.radioSourceCallback)
        
        self.w.checkboxUC = CheckBox((10, 125, 45, 20), "UC", callback=self.checkboxUCcallback)
        self.w.checkboxLC = CheckBox((55, 125, 50, 20), "LC", callback=self.checkboxLCcallback)
        
        self.w.sourceGlyph = ComboBox((105, 125, 85, 21), gName, callback=self.sourceGlyphCallback, completes=False, continuous=True)
        
        self.w.button = Button((10, 159, -10, 20), "OK", callback=self.buttonCallback)  


    def radioTargetCallback(self, sender):

        self.targetIndex = sender.get()

        
    def radioSourceCallback(self, sender):

        self.sourceIndex = sender.get()

    
    def checkboxUCcallback(self, sender):
        
        pass

    
    def checkboxLCcallback(self, sender):
    
        pass
    
    
    def sourceGlyphCallback(self, sender):
        
       self.gSource = f[sender.get()]
               
        # for lets in gName:
        #     if sender.get() != lets:
        #         Message("no match")
        #         break

                             
    def buttonCallback(self, sender):
        
        self.compute_sidebearings()
        self.w.close()

    def compute_sidebearings(self):
        if self.targetIndex == 0:
            if self.sourceIndex == 0:
                for gTarget in gList:
                    gTarget.leftMargin = self.gSource.leftMargin
            elif self.sourceIndex == 1:
                for gTarget in gList:
                    gTarget.leftMargin = self.gSource.rightMargin
        elif self.targetIndex == 1:
            if self.sourceIndex == 0:
                for gTarget in gList:
                    gTarget.rightMargin = self.gSource.leftMargin
            elif self.sourceIndex == 1:
                for gTarget in gList:
                    gTarget.rightMargin = self.gSource.rightMargin

        
SideBearing()

"""
---------------
     TO DO
---------------
+ A pop-up message that alerts user when inputted source glyph doesn't exist in current font
+ Limited list of source glyphs (no accented chars, etc.) OR
+ Checkbox to filter UC, lc, numbers, etc.
+ Fallbacks for empty or invalid entries (glyphs not in font, etc.)

"""
