from robofab.interface.all.dialogs import Message
from vanilla import *

f = CurrentFont()

currentHeight = f.info.ascender + -f.info.descender #Total measurement from ascender to descender


class ScaleAMucci(object):

    def __init__(self):
        
        self.buildUI()
        self.w.open()
        
    def buildUI(self):
        
        self.w = Window((300, 155))
        
        self.w.currentHeightText = TextBox((10, 10, -10, 17),
                                   "Current height:   " + str(currentHeight) + " em units")
        
        self.w.targetHeightSlider = Slider((10, 40, -10, 23),
                                    minValue = currentHeight*.5,
                                    maxValue = currentHeight*1.5,
                                    value = currentHeight,
                                    tickMarkCount=10,
                                    callback=self.sliderCallback)

        self.w.targetHeightText = TextBox((10, 82, 100, 17),
                                  "Target height:")
         
        self.w.targetHeightInput = EditText((115, 80, 55, 21),
                                   currentHeight,
                                   callback=self.targetHeightInputCallback)
        
        self.w.okButton = Button((10, 105, -10, 40),
                          "Scale-a-mooch!",
                          callback=self.okButtonCallback)
        
         
    def sliderCallback(self, sender):
        self.targetHeight = int(sender.get())
         
        self.w.targetHeightInput.set(self.targetHeight)
         
    def targetHeightInputCallback(self, sender):
        self.targetHeight = int(sender.get())
         
        self.w.targetHeightSlider.set(self.targetHeight)
        
    
    def mainCalculation(self):
        try:    
            #Convert input string to integers & calculate scale
            xFactor = self.targetHeight / currentHeight
    
            #Decompose every glyph first (in case of component-based font)
            for glyph in f:
                glyph.decompose()

            #Scale & tans every glyph
            for glyph in f:
                glyph.width *= xFactor
                glyph.scale((xFactor))
                glyph.mark = (0.69, 0.43, 0.18, 1)

            #Modify vertical metrics to new dimensions    
            f.info.ascender *= xFactor
            f.info.capHeight *= xFactor
            f.info.xHeight *= xFactor
            f.info.descender *= xFactor

            Message("Nice tan!")

        #In case user inputs strings that can't be converted to integers
        except ValueError:
            Message("The Mooch only likes numbers!")

        
    def okButtonCallback(self, sender):
        self.mainCalculation()
        self.w.close()


ScaleAMucci()

"""
---------------
     TO DO
---------------
+ BUG: Weird combo box bug that repeats characters that proceed the first (e.g. typing "de" yields "dee," "deg" yields "deegg")
+ BUG: Invalid glyphs also get doubled (anything not in UC & lc)

+ Restrict text input to numerals only
+ Round results (esp. side bearings) to closest integer
+ "Scale" or move guides
+ Visual display to illustrate what different values do to a textblock

"""
