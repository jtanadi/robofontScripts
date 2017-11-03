from vanilla import *
from drawBot import *
from drawBot.ui.drawView import DrawView
from fontTools.pens.cocoaPen import CocoaPen
from numpy import arange
from lib.UI.spaceCenter.glyphSequenceEditText import GlyphSequenceEditText
from datetime import datetime

f = CurrentFont()

if f is not None:
    
    # Font Info
    xHeightCurrent = f.info.xHeight
    ascender = f.info.ascender - xHeightCurrent
    descender = f.info.descender
    fontName = f.info.familyName + " " + f.info.styleName

    # File Info
    fileName = f.path.split("/")[-1]
    filePath = f.path.rstrip(fileName)
    fileToSave = filePath + '/' + fileName + '_SKETCH' + '.pdf'


else:
    xHeightCurrent = 500
    ascender = 250
    descender = -250
    fontName = "No open font"
    
# Page Setup / starting values
ppi = 72  # default drawBot value
marginTop = 54
marginLBR = 30
firstXHeightLine = 528

pageWidth = width()
pageHeight = height()

xHeightTarget = 0.5 * ppi
xFactor = xHeightTarget / xHeightCurrent
ascenderTarget = ascender * xFactor
descenderTarget = descender *xFactor

class EtchASketch(object):
    
    def __init__(self):
                
        self.buildUI()
        Drawing().pageSetup()
        self.refreshCanvas()
        self.w.open()
        
    # def refreshCanvas(self):
    #     pdf = pdfImage()
    #     self.w.canvas.setPDFDocument(pdf)
        
    def buildUI(self):    
        
        self.w = Window((960,590),
                 minSize = (830,500),
                 title = "Etch-A-Sketch: " + fontName)
        
        self.w.canvas = DrawView((220, 10, -10, -10))
            
        
class Drawing():
            
    def pageSetup(self):
       
        newDrawing()
        newPage("LetterLandscape")
        
        def _drawHeader():
        
            self.dateTime = datetime.today().strftime("%m/%d/%y – %I:%M%p")
        
            font("VulfMono-Light")
            fallbackFont("Courier")
            fontSize(8)
            text(fontName + " – " + self.dateTime, (marginLBR, pageHeight-27))

            stroke(0, 0, 0, 1)
            strokeWidth(0.5)
            line((marginLBR, pageHeight-40.5), (pageWidth-marginLBR, pageHeight-40.5))
            
            
        _drawHeader()
    #     self.refreshCanvas()
        
    def refreshCanvas(self):
        pdf = pdfImage()
        EtchASketch().buildUI().w.canvas.setPDFDocument(pdf)
        
EtchASketch()    