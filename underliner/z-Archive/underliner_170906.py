from vanilla import *
from mojo.canvas import Canvas
from fontTools.pens.cocoaPen import CocoaPen
from mojo.drawingTools import *

f = CurrentFont()

class Underliner(object):
    
    def __init__(self):
        
        self.offset = 250
        self.thickness = 250
        
        self.text = ""
        
        self.buildUI()
        self.w.open()


    def buildUI(self):
        
        self.w = Window((500, 410),
                 "Underline all your glyphs!")
        
        self.w.offsetText = TextBox((10, 10, -10, 20),
                              "Offset")
                              
        self.w.offsetValue = EditText((100, 8, 50, 22),
                             self.offset,
                             callback = self.offsetValueCallback)
        
        self.w.offsetSlider = Slider((10, 25, -10, 40),
                              minValue = 0,
                              maxValue = 500,
                              value = 250,
                              callback = self.offsetSliderCallback)
                        
        self.w.thicknessText = TextBox((10, 70, -10, 20),
                               "Thickness")    
                               
        self.w.thicknessValue = EditText((100, 68, 50, 22),
                                self.thickness,
                                callback = self.thicknessValueCallback)                    
                        
        self.w.thicknessSlider = Slider((10, 85, -10, 40),
                                 minValue = 0,
                                 maxValue = 500,
                                 value = 250,
                                 callback = self.thicknessSliderCallback)
                                
        self.w.drawButton = Button((10, 115, -10, 40),
                            "Underline",
                            callback = self.drawButtonCallback)
                            
        self.w.canvas = Canvas((10, 160, -10, -43),
                        hasHorizontalScroller = False,
                        hasVerticalScroller = False,
                        delegate = self)
                        
        self.w.inputString = EditText((10, 375, -10, 24),
                             callback = self.inputStringCallback)                                                
                            
    
    def offsetSliderCallback(self, sender):
        
        self.offset = int(sender.get())
        
        self.w.offsetValue.set(self.offset)
        
        self.w.canvas.update()
        

    def thicknessSliderCallback(self, sender):
        
        self.thickness = int(sender.get())
        
        self.w.thicknessValue.set(self.thickness)
        
        self.w.canvas.update()
        
    
    def offsetValueCallback(self, sender):
        
        self.offset = int(sender.get())
        
        self.w.offsetSlider.set(self.offset)
        
        self.w.canvas.update()
        
        
    def thicknessValueCallback(self, sender):
        
        self.thickness = int(sender.get())
        
        self.w.thicknessSlider.set(self.thickness)
        
        self.w.canvas.update()    
    
    
    def inputStringCallback(self, sender):
        self.text = sender.get()
        
        self.w.canvas.update()
        
        
    def draw(self):
        
        fill(0,0,0, .5)
        stroke(0,0,0, 1)
        
        translate(10,80)
        scale(.1)
        
        for g in self.text:
            pen = CocoaPen(f)
            f[g].draw(pen)
            drawPath(pen.path)
            rect(-10, -self.offset, f[g].width+20, -self.thickness)
            translate(f[g].width, 0)
            
            
    def drawUnderline(self):

        f.decompose()
        
        for glyph in f:
            #glyph.correctDirection()
            
            glyphWidth = glyph.width
            
            pen = glyph.getPen()

            pen.moveTo((-10, -self.offset)) #start at -5 left of left SB at inputted offset (to get rid of white lines)
            pen.lineTo((glyphWidth+10, -self.offset)) #draw a line to +5 right of right SB (to get rid of white lines)
            pen.lineTo((glyphWidth+10, -self.offset-self.thickness)) #draw a line down from offset to inputted thickness
            pen.lineTo((-10, -self.offset-self.thickness))
            pen.lineTo((-10, -self.offset))
            pen.closePath()
            
            
    def drawButtonCallback(self, sender):
        
        self.drawUnderline()
        
        self.w.canvas.update()
        

Underliner()

"""
---------------
     TO DO
---------------
+ BUG: Crashes when script is run & CurrentFont() is None
+ BUG: Crashes when using non-alphabet chars in sample string
+ BUG: Why does correctDirection() not work???

+ Can input string EditText have default focus when script is launched?
+ Drawing auto-resizes based on input width

"""