from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen

f = CurrentFont()
g = f["a"]
           
class ExampleWindow:

    def __init__(self):
        self.size = 0.2

        self.w = Window((400, 400))
        
        self.w.slider = Slider((10, 5, -10, 22),
                        minValue = 0,
                        maxValue = 0.8,
                        value=self.size,
                        callback=self.sliderCallback)
                        
        self.w.button = Button((10, 50, -10, 22),
                        "ok",
                        callback=self.buttonCallback)
                                        
        self.w.open()
        
        #self.drawLetter()
    
    def sliderCallback(self, sender):
        self.size = sender.get()
        
   
    def drawLetter(self):
        newPage(300,300)
        pen = CocoaPen(f)

        fill(0,0,0, 0.5)
        stroke(0,0,0,1)

        translate(0,80)
        scale(self.size)
        g.draw(pen)

        drawPath(pen.path) 
    
    
    def buttonCallback(self, sender):
        self.drawLetter()            
        
           

ExampleWindow()