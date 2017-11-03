from mojo.canvas import Canvas
from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen
from mojo.drawingTools import *

f = CurrentFont()
g = f["g"]
    
class GlyphWindow:

    def __init__(self):
        self.size = 0.25

        self.w = Window((400, 400))
        
        self.w.slider = Slider((10, 5, -10, 22),
                        minValue = 0.1,
                        maxValue = 0.4,
                        value=self.size,
                        callback=self.sliderCallback)
                        
        self.w.canvas = Canvas((10, 30, -10, -10),
                        hasHorizontalScroller = False,
                        hasVerticalScroller = False,
                        delegate=self)
                
        self.w.open()


    def sliderCallback(self, sender):
        self.size = sender.get()
              
        self.w.canvas.update()
    

    def draw(self):
        #rect(10, 10, self.size, self.size)
        pen = CocoaPen(f)
        
        fill(0,0,0, 0.5)
        stroke(0,0,0,1)
        
        translate(0,80)
        scale(self.size)
        g.draw(pen)
        drawPath(pen.path)  
       
GlyphWindow()