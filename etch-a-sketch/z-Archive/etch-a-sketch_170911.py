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
    
# Initial values
ppi = 72  # default drawBot value
marginTop = 54
marginLBR = 30
firstXHeightLine = 528

# Have to define these instead of using width() and height(), otherwise it doesn't work the first time script is run
pageWidth = 792
pageHeight = 612

xHeightTarget = 0.5 * ppi
xFactor = xHeightTarget / xHeightCurrent
ascenderTarget = ascender * xFactor
descenderTarget = descender * xFactor


class EtchASketch(object):
    
    def __init__(self):

        self.ascenderBox = 0
        self.descenderBox = 0
        self.grayLettersBox = 0
        self.blueLinesBox = 0
                
        self.buildUI()
        self.makeDrawing()
        
        self.w.open()
        
    
    def buildUI(self):    
        
        self.w = Window((960,590),
                 minSize = (830,500),
                 title = "Etch-A-Sketch: " + fontName)
        
                    
                
        self.w.xHeightText = TextBox((8, 48, 200, 17),
                             "x-Height")
        
        self.w.xHeightSlider = Slider((12, 70, 194, 23),
                               minValue = 0.5,
                               maxValue = 2,
                               value = xHeightTarget/ppi,
                               tickMarkCount = 7,
                               stopOnTickMarks = True,
                               callback = self.xHeightSliderCallback)
                               
        self.w.xHeightMinVal = TextBox((8, 95, 50, 17),
                               "0.5")
                               
        self.w.xHeightMidVal = TextBox((95, 95, 50, 17),
                               "1.25")                               
        
        self.w.xHeightMaxVal = TextBox((185, 95, 50, 17),
                               "2.0")
        
        self.w.guidesText = TextBox((8, 145, 100, 17),
                            "Guides")
                            
        self.w.ascenderCheckbox = CheckBox((10, 165, 100, 22),
                                  "Ascender",
                                  callback = self.ascenderCheckboxCallback)
                                  
        self.w.descenderCheckbox = CheckBox((10, 187, 100, 22),
                                  "Descender",
                                  callback = self.descenderCheckboxCallback)
        
        self.w.extrasText = TextBox((8, 245, 100, 17),
                            "Extras")
        
        self.w.blueLinesCheckbox = CheckBox((10, 265, 150, 22),
                                   "Non-photo blue lines",
                                   callback = self.blueLinesCheckboxCallback)
                                   
        self.w.grayLettersCheckbox = CheckBox((10, 287, 150, 22),
                                   "Gray letters",
                                   callback = self.grayLettersCheckboxCallback)
                                  
        self.w.printButton = SquareButton((10, 430, 200, -10),
                            "Print!\n(cmd + p)",
                            callback = self.printButtonCallback)
                            
        self.w.printButton.bind('p', ["command"])
         
        self.w.canvas = DrawView((220, 10, -10, -10))
        
        if f is not None:
            self.w.inputText = GlyphSequenceEditText((10, 10, 200, 22),
                               f.naked(),
                               callback = self.inputTextCallback)
                               
            self.w.saveButton = SquareButton((10, 370, 200, 50),
                                "Save PDF!",
                                callback = self.saveButtonCallback)
                    
        else:
            self.w.inputText = EditText((10, 10, 200, 22),
                               "No open font")
                               
            self.w.inputText.enable(False)
            
            self.w.grayLettersCheckbox.enable(False)
        

    def inputTextCallback(self, sender):
        
        self.inputText = sender.get()
        
        self.makeDrawing()
        
        
    def xHeightSliderCallback(self, sender):
        
        global xHeightTarget, xFactor, ascenderTarget, descenderTarget
        
        xHeightTarget = sender.get() * ppi
        xFactor = xHeightTarget / xHeightCurrent
        ascenderTarget = ascender * xFactor
        descenderTarget = descender *xFactor
        
        self.makeDrawing()
        
    
    def ascenderCheckboxCallback(self, sender):
        
        self.ascenderBox = sender.get()
        
        self.makeDrawing()
    
    
    def descenderCheckboxCallback(self, sender):
        
        self.descenderBox = sender.get()
                
        self.makeDrawing()

    
    def grayLettersCheckboxCallback(self, sender):
        
        self.grayLettersBox = sender.get()
        
        self.makeDrawing()
    
        
    def blueLinesCheckboxCallback(self, sender):
        
        self.blueLinesBox = sender.get()
        
        self.makeDrawing()
    
        
    def saveButtonCallback(self, sender):
        
        self.makeDrawing()
        saveImage(fileToSave)
        
        self.w.close()
    
    
    def printButtonCallback(self, sender):
        
        self.makeDrawing()
        printImage()

        
# DRAWING STUFF BELOW
    
    def makeDrawing(self):
        
        def pageSetup():
               
            def _drawHeader():
        
                self.dateTime = datetime.today().strftime("%m/%d/%y – %I:%M%p")
            
                cmykFill(0, 0, 0, 1, 1)
                cmykStroke(None)
                font("VulfMono-Light")
                fallbackFont("Courier")
                fontSize(8)
                text(fontName + " – " + self.dateTime, (marginLBR, pageHeight-27))

                cmykFill(None)
                cmykStroke(0, 0, 0, 1, 1)
                strokeWidth(0.5)
                line((marginLBR, pageHeight-40.5), (pageWidth-marginLBR, pageHeight-40.5))

        
            def _drawSketchLines(xHeightList, baselineList):        
                
                cmykFill(None)
                
                if self.blueLinesBox == 1:
                    cmykStroke(.31, .07, 0, .07, 1)
                    strokeWidth(0.5)
                    
                else:
                    cmykStroke(0, 0, 0, .35, 1)
                    strokeWidth(0.5)
                        
                for xHeight in xHeightList:
                    line((marginLBR, xHeight), (pageWidth - marginLBR, xHeight)) # x-height line
            
                for baseline in baselineList:                     
                    line((marginLBR, baseline), (pageWidth - marginLBR, baseline)) # baseline
                
                
            def _drawAscender(xHeightlist):
            
                cmykFill(None)
                cmykStroke(1, 1, 0, 0, 1)
                strokeWidth(0.5)
            
                for xHeight in xHeightList:
                    line((marginLBR, xHeight + ascenderTarget), (pageWidth - marginLBR, xHeight + ascenderTarget))
    
                         
            def _drawDescender(baselineList):
                
                cmykFill(None)
                cmykStroke(0, 1, 1, 0, 1)
                strokeWidth(0.5)
                            
                for baseline in baselineList:
                    line((marginLBR, baseline + descenderTarget), (pageWidth - marginLBR, baseline + descenderTarget))
            
                
            def _checkAscDesc(xHeightList, baselineList):
                
                if self.ascenderBox and self.descenderBox == 1:                
                    _drawAscender(xHeightList)
                    _drawDescender(baselineList)
            
                elif self.ascenderBox == 1:
                    _drawAscender(xHeightList)
        
                elif self.descenderBox == 1:
                    _drawDescender(baselineList)
            
            
            def _calculateSketchLines():
            
                spacerRange = arange(0, 15, 2.5)
            
                baselineList = []
                xHeightList = []        
            
                for i in spacerRange:
                    spacer = i * xHeightTarget
                                        
                    xHeightList.append(firstXHeightLine - spacer)
                    baselineList.append(firstXHeightLine - spacer - xHeightTarget)
            
                return xHeightList, baselineList
                
                
            xHeightList = _calculateSketchLines()[0]
            baselineList = _calculateSketchLines()[1]
            
            newDrawing()
            newPage("LetterLandscape")

            _drawHeader()
            _calculateSketchLines()
            _drawSketchLines(xHeightList, baselineList)
            _checkAscDesc(xHeightList, baselineList)
                
            self.refreshCanvas()

        
        def drawLetters():        
    
            # Check if this class has inputText before drawing letters
            # This helps with scaling & saving functions
            if hasattr(self, "inputText"):
                
                if self.grayLettersBox == 1:              
                    cmykFill(0, 0, 0, .15, 1)
                    cmykStroke(None)
                    
                else:
                    cmykFill(0, 0, 0, 1, 1)
                    cmykStroke(None)
  
                translate(marginLBR, firstXHeightLine-xHeightTarget)
                for g in self.inputText:
            
                    pen = CocoaPen(f)
            
                    scale(xFactor)
            
                    f[g].draw(pen)
                    drawPath(pen.path)
                    translate(f[g].width, 0)
            
                    scale(1/xFactor)

                self.refreshCanvas()
         
        pageSetup()
        drawLetters()
                 
    def refreshCanvas(self):
        pdf = pdfImage()
        self.w.canvas.setPDFDocument(pdf)

EtchASketch()

"""
---------------
     TO DO
---------------
+ Is it possible to separate into 2 classes? Some parts/processes might have to be re-thought / re-written?
+ Make a DrawingTools version so it's not reliant on DrawBot
+ Better way of dividing page & making sketch lines (e.g. different count & location depending on x-height range)
+ 

"""
