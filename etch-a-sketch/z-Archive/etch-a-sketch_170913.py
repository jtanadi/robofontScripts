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
    fontName = str(f.info.familyName + " " + f.info.styleName)

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


def calculateMetrics(xHeightTarget):

    xFactor = xHeightTarget / xHeightCurrent
    ascenderTarget = ascender * xFactor
    descenderTarget = descender * xFactor

    return xFactor, ascenderTarget, descenderTarget


class EtchASketch(object):
    
    def __init__(self):
            
        self.ascenderBox = self.descenderBox = self.grayLettersBox = self.blueLinesBox = 0
        self.xHeightTarget = 0.5 * ppi
        self.inputText = ""
        
        self.drawing = Drawing(self.xHeightTarget, self.inputText, self.ascenderBox,
                               self.descenderBox, self.blueLinesBox, self.grayLettersBox)
        
        self.buildUI()
        self.refreshCanvas()
        self.w.open()
        
    
    def buildUI(self):    
        
        self.w = Window((960,590),
                 minSize = (830,500),
                 title = "Etch-A-Sketch: " + fontName)
 
        self.w.xHeightText = TextBox((8, 48, 200, 17),
                             "x-Height (in.)")
        
        self.w.xHeightSlider = Slider((12, 70, 194, 23),
                               minValue = 0.5,
                               maxValue = 2,
                               value = self.xHeightTarget / ppi,
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
        
        self.drawing.inputTextDrawing = self.inputText
        self.refreshCanvas()
        
        
    def xHeightSliderCallback(self, sender):
        
        self.xHeightTarget = sender.get() * ppi
        calculateMetrics(self.xHeightTarget)
                        
        self.drawing.xHeightDrawing = self.xHeightTarget
        self.refreshCanvas()
        
    
    def ascenderCheckboxCallback(self, sender):
        
        self.ascenderBox = sender.get()
        
        self.drawing.ascenderBoxDrawing = self.ascenderBox
        self.refreshCanvas()

    
    def descenderCheckboxCallback(self, sender):
        
        self.descenderBox = sender.get()
                
        self.drawing.descenderBoxDrawing = self.descenderBox
        self.refreshCanvas()

    
    def grayLettersCheckboxCallback(self, sender):
        
        self.grayLettersBox = sender.get()
        
        self.drawing.grayLettersBoxDrawing = self.grayLettersBox
        self.refreshCanvas()
    
        
    def blueLinesCheckboxCallback(self, sender):
        
        self.blueLinesBox = sender.get()
        
        self.drawing.blueLinesBoxDrawing = self.blueLinesBox
        self.refreshCanvas()
    
        
    def saveButtonCallback(self, sender):
        
        self.refreshCanvas()
        saveImage(fileToSave)
        
        self.w.close()
    
    
    def printButtonCallback(self, sender):
        
        self.refreshCanvas()
        printImage()
    
    
    def refreshCanvas(self):
        self.drawing.pageSetup()
        self.drawing.drawLetters()
        
        pdf = pdfImage()
        self.w.canvas.setPDFDocument(pdf)


class Drawing():
    
    def __init__(self, xHeightTarget, inputText, ascenderBox,
                 descenderBox, blueLinesBox, grayLettersBox):
 
        self.xHeightDrawing = xHeightTarget
        self.inputTextDrawing = inputText
        self.ascenderBoxDrawing = ascenderBox
        self.descenderBoxDrawing = descenderBox
        self.blueLinesBoxDrawing = blueLinesBox
        self.grayLettersBoxDrawing = grayLettersBox
        
        self.pageSetup()
        
            
    def pageSetup(self):
           
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
            strokeWidth(0.5)
            
            if self.blueLinesBoxDrawing == 1:
                cmykStroke(.31, .07, 0, .07, 1)
                                   
            else:
                cmykStroke(0, 0, 0, .35, 1)
                    
            for xHeight in xHeightList:
                line((marginLBR, xHeight), (pageWidth - marginLBR, xHeight)) # x-height line
        
            for baseline in baselineList:                     
                line((marginLBR, baseline), (pageWidth - marginLBR, baseline)) # baseline
            
            
        def _drawAscender(xHeightlist, ascenderTarget):
            
            cmykFill(None)
            lineDash(3)
            strokeWidth(0.5)
            
            if self.blueLinesBoxDrawing == 1:
                cmykStroke(.31, .07, 0, .07, 1)

            else:
                cmykStroke(0, 0, 0, .35, 1)
            
            for xHeight in xHeightList:
                line((marginLBR, xHeight + ascenderTarget),
                     (pageWidth - marginLBR, xHeight + ascenderTarget))

                     
        def _drawDescender(baselineList, descenderTarget):

            cmykFill(None)
            lineDash(3)
            strokeWidth(0.5)
            
            if self.blueLinesBoxDrawing == 1:
                cmykStroke(.31, .07, 0, .07, 1)

            else:
                cmykStroke(0, 0, 0, .35, 1)

            for baseline in baselineList:
                line((marginLBR, baseline + descenderTarget), (pageWidth - marginLBR, baseline + descenderTarget))
        
            
        def _checkAscDesc(xHeightList, baselineList):
            
            if self.ascenderBoxDrawing and self.descenderBoxDrawing == 1:                
                _drawAscender(xHeightList, ascenderTarget)
                _drawDescender(baselineList, descenderTarget)
        
            elif self.ascenderBoxDrawing == 1:
                _drawAscender(xHeightList, ascenderTarget)
    
            elif self.descenderBoxDrawing == 1:
                _drawDescender(baselineList, descenderTarget)
        
        
        def _calculateSketchLines():
        
            spacerRange = arange(0, 15, 2.5)
        
            baselineList = []
            xHeightList = []        
        
            for i in spacerRange:
                spacer = i * self.xHeightDrawing
                                    
                xHeightList.append(firstXHeightLine - spacer)
                baselineList.append(firstXHeightLine - spacer - self.xHeightDrawing)
        
            return xHeightList, baselineList
            
            
        xHeightList = _calculateSketchLines()[0]
        baselineList = _calculateSketchLines()[1]
        ascenderTarget = calculateMetrics(self.xHeightDrawing)[1]
        descenderTarget = calculateMetrics(self.xHeightDrawing)[2]
        
        newDrawing()
        newPage("LetterLandscape")

        _drawHeader()
        _calculateSketchLines()
        _drawSketchLines(xHeightList, baselineList)
        _checkAscDesc(xHeightList, baselineList)
        
        
    def drawLetters(self):        
            
        xFactor = calculateMetrics(self.xHeightDrawing)[0]
        
        if self.grayLettersBoxDrawing == 1:              
            cmykFill(0, 0, 0, .15, 1)
            cmykStroke(None)
            
        else:
            cmykFill(0, 0, 0, 1, 1)
            cmykStroke(None)
  
        translate(marginLBR, firstXHeightLine-self.xHeightDrawing)
        
        for g in self.inputTextDrawing:
    
            pen = CocoaPen(f)
    
            scale(xFactor)
    
            f[g].draw(pen)
            drawPath(pen.path)
            translate(f[g].width, 0)
    
            scale(1/xFactor)

                 
EtchASketch()

"""
---------------
     TO DO
---------------
+ Make a DrawingTools version so it's not reliant on DrawBot - (is it worth it?)
+ Better way of dividing page & making sketch lines (e.g. different count & distance depending on x-height range)
+ Expand to have typecooker mode?
+ Allow inputText string to flow to 2nd line
"""
