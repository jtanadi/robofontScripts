from mojo.UI import Message
from vanilla import *
from mojo.drawingTools import *
from mojo.canvas import Canvas

f = CurrentFont()

if f == None:
    Message("Open a font first!")

upm = f.info.unitsPerEm
currentHeight = int(f.info.ascender + -f.info.descender) #Total measurement from ascender to descender

class ScaleAMucci(object):

    def __init__(self):
        
        self.targetHeight = currentHeight
        self.buildUI()
        self.w.open()
        
        
    def buildUI(self):
        
        self.w = Window((300, 415))
        
        self.w.currentHeightText = TextBox((10, 10, 150, 17),
                                   "Current height:   " + str(currentHeight))
                                   
        self.w.currentUPM = TextBox((200, 10, -10, 17),
                                   "UPM:   " + str(upm),
                                   alignment = "right")                                   
        
        self.w.targetHeightSlider = Slider((10, 40, -10, 23),
                                    minValue = currentHeight*.5,
                                    maxValue = currentHeight*1.5,
                                    value = currentHeight,
                                    callback=self.sliderCallback)

        self.w.targetHeightText = TextBox((10, 82, 100, 17),
                                  "Target height:")
         
        self.w.targetHeightInput = EditText((115, 80, 55, 21),
                                   currentHeight,
                                   callback=self.targetHeightInputCallback)
        
        self.w.okButton = Button((10, 105, -10, 40),
                          "Scale-a-mooch!",
                          callback=self.okButtonCallback)
                          
        self.w.canvas = Canvas((0, 150, 0, 0),
                        hasHorizontalScroller = False,
                        hasVerticalScroller = False,
                        delegate = self)                          
        
         
    def sliderCallback(self, sender):
        
        self.targetHeight = int(sender.get())
         
        self.w.targetHeightInput.set(self.targetHeight)
        
        self.w.canvas.update()

         
    def targetHeightInputCallback(self, sender):
        
        self.targetHeight = int(sender.get())
         
        self.w.targetHeightSlider.set(self.targetHeight)
        
        self.w.canvas.update()
        
    
    def mainCalculation(self):

        try:    
            #Calculate scale
            xFactor = self.targetHeight / currentHeight
    
            #Decompose every glyph first (in case of component-based font)
            for glyph in f:
                glyph.decompose()

            #Scale & tans every glyph
            for glyph in f:
                glyph.scale(xFactor)
                glyph.width *= xFactor
                glyph.round() #Rounds all float values (incl. side bearings)
                                
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
    
    
    def draw(self):
        
        fill(0,0,0,.5)
        stroke(1,1,1,.25)
        scale = self.targetHeight/upm
        height = 50*scale
        
        for y in range(25, 225, 50):            
            rect(10, y, 278, height)
        

ScaleAMucci()

"""
---------------
     TO DO
---------------
+ Restrict text input to numerals only
+ "Scale" or move guides
"""
