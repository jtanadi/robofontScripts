from mojo.canvas import Canvas
from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen
from mojo.drawingTools import *

f = CurrentFont()
    
class GlyphWindow:

    def __init__(self):
        self.size = 0.25
        self.text = "hei"
        
        self.w = Window((400, 400))
        
        self.w.slider = Slider((10, 5, -10, 22),
                        minValue = 0.1,
                        maxValue = 0.4,
                        value=self.size,
                        callback=self.sliderCallback)
                        
        self.w.editText = EditText((10, 30, -10, 25), "", callback = self.editTextCallback)
                        
        self.w.canvas = Canvas((10, 65, -10, -10),
                        hasHorizontalScroller = False,
                        hasVerticalScroller = False,
                        delegate=self)
                
        self.w.open()


    def editTextCallback(self, sender):
        self.text = sender.get()
        

    def sliderCallback(self, sender):
        self.size = sender.get()
              
        self.w.canvas.update()
    
    
    def draw(self):

        
        fill(0,0,0, 0.45)
        stroke(0,0,0, 1)
        
        translate(0,80)
        scale(self.size)
        
        for g in self.text:
            pen = CocoaPen(f)
            f[g].draw(pen)
            drawPath(pen.path)
            translate(f[g].width, 0)  
       
GlyphWindow()