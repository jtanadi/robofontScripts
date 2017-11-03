import drawBot
from drawBot.ui.drawView import DrawView
from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen

f = CurrentFont()
dpi = 72
currentXheight = f.info.xHeight

class LetterTester(object):
    
    def __init__(self):
        self.text = ""
        self.targetXheight = 1.25*dpi
        
    
        self.w = Window((500,500),
                 minSize = (500,500),
                 title = "Tester")
        
        self.w.editText = EditText((10, 10, -10, 24),
                          "",
                          callback = self.editTextCallback)
        
        self.w.xHeightSlider = Slider((10, 40, -10, 24),
                               value = 1.25,
                               minValue = 0.5,
                               maxValue = 2,
                               callback = self.xHeightSliderCallback)
        
        self.w.canvas = DrawView((10, 70, -10, -10))
        
        self.draw()
        
        self.w.open()
        
    def editTextCallback(self, sender):
        self.text = sender.get()
        
        self.draw()
        
    def xHeightSliderCallback(self, sender):
        self.targetXheight = sender.get()*dpi
        
        self.draw()
        
    def draw(self):    
        self.xFactor = self.targetXheight / currentXheight
        
        drawBot.newDrawing()
        drawBot.newPage("LetterLandscape")
        
        pageWidth = drawBot.width()

        drawBot.fill(0,0,0, 0.5)
        drawBot.stroke(0,0,0,1)

        drawBot.rect(.5*dpi,.5*dpi,pageWidth-(1*dpi),self.targetXheight)

        drawBot.translate(0.5*dpi,.5*dpi)
        drawBot.scale(self.xFactor)

        for g in self.text:
            pen = CocoaPen(f)
            f[g].draw(pen)
            drawBot.drawPath(pen.path)
            drawBot.translate(f[g].width, 0)
            
        pdf = drawBot.pdfImage()
        # set the pdf data in the canvas
        self.w.canvas.setPDFDocument(pdf)
        

LetterTester()
        
    