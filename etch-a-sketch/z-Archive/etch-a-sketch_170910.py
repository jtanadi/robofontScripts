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

        self.ascenderBox = 0
        self.descenderBox = 0
        self.blueLinesBox = 0
                
        self.buildUI()
        self.pageSetup()
        
        self.w.open()
        
    
    def buildUI(self):    
        
        self.w = Window((960,590),
                 minSize = (830,500),
                 title = "Etch-A-Sketch: " + fontName)
        
        if f is not None:
            self.w.inputText = GlyphSequenceEditText((10, 10, 200, 22),
                               f.naked(),
                               callback = self.inputTextCallback)
                               
        else:
            self.w.inputText = EditText((10, 10, 200, 22),
                               "No open font")
            self.w.inputText.enable(False)
                
        self.w.xHeightText = TextBox((10, 48, 200, 17),
                             "x-Height")
        
        self.w.xHeightSlider = Slider((15, 70, 190, 23),
                               minValue = 0.5,
                               maxValue = 2,
                               value = xHeightTarget/ppi,
                               tickMarkCount = 7,
                               stopOnTickMarks = True,
                               callback = self.xHeightSliderCallback)
                               
        self.w.xHeightMinVal = TextBox((10, 95, 50, 17),
                               "0.5")
                               
        self.w.xHeightMidVal = TextBox((95, 95, 50, 17),
                               "1.25")                               
        
        self.w.xHeightMaxVal = TextBox((185, 95, 50, 17),
                               "2.0")
                                       
        self.w.ascenderCheckbox = CheckBox((10, 150, 100, 22),
                                  "Ascender",
                                  callback = self.ascenderCheckboxCallback)
                                  
        self.w.descenderCheckbox = CheckBox((10, 172, 100, 22),
                                  "Descender",
                                  callback = self.descenderCheckboxCallback)

        self.w.printButton = SquareButton((10, 265, 200, 125),
                            "Print!\n(cmd + p)",
                            callback = self.printButtonCallback)
                            
        self.w.printButton.bind('p', ["command"])
        
        self.w.saveButton = SquareButton((10, 400, 200, 50),
                            "Save PDF!",
                            callback = self.saveButtonCallback)
                            
        if f is None:
            self.w.saveButton.show(False)
                                                              
        self.w.blueLinesCheckbox = CheckBox((10, -30, 150, 22),
                                  "Non-photo blue lines",
                                  callback = self.blueLinesCheckboxCallback)
        
        self.w.canvas = DrawView((220, 10, -10, -10))
        

    def inputTextCallback(self, sender):
        
        self.inputText = sender.get()
        
        self.pageSetup()
        self.drawLetters()
        
        
    def xHeightSliderCallback(self, sender):
        
        global xHeightTarget, xFactor, ascenderTarget, descenderTarget
        
        xHeightTarget = sender.get() * ppi
        xFactor = xHeightTarget / xHeightCurrent
        ascenderTarget = ascender * xFactor
        descenderTarget = descender *xFactor
        
        self.pageSetup()
        
        # Check if this class has inputText before calling the drawLetters function
        # (This helps to scale the drawing *before* inputting string)
        if hasattr(self, "inputText"):
            self.drawLetters()

    
    def ascenderCheckboxCallback(self, sender):
        
        self.ascenderBox = sender.get()
        
        self.pageSetup()
        self.drawLetters()

    
    def descenderCheckboxCallback(self, sender):
        
        self.descenderBox = sender.get()
                
        self.pageSetup()
        self.drawLetters()

        
    def blueLinesCheckboxCallback(self, sender):
        
        self.blueLinesBox = sender.get()
        
        self.pageSetup()
        self.drawLetters()

    
    def printButtonCallback(self, sender):
        
        self.pageSetup()
        self.drawLetters()
        printImage()

        
    def saveButtonCallback(self, sender):
        
        self.pageSetup()
        self.drawLetters()
        saveImage(fileToSave)
        
        self.w.close()
    
        
    def pageSetup(self):
       
        newDrawing()
        newPage("LetterLandscape")
        
        def _drawHeader():
        
            # Think about moving this to its own def, so callable when print button is hit, too
            # When should date stamp happen? Print, PDF, every time header is drawn??
            self.dateTime = datetime.today().strftime("%m/%d/%y – %I:%M%p")
        
            font("VulfMono-Light")
            fallbackFont("Courier")
            fontSize(8)
            text(fontName + " – " + self.dateTime, (marginLBR, pageHeight-27))

            stroke(0, 0, 0, 1)
            strokeWidth(0.5)
            line((marginLBR, pageHeight-40.5), (pageWidth-marginLBR, pageHeight-40.5))
        
        
        def _drawSketchLines():        

            spacerRange = arange(0, 15, 2.5)
        
            baselineList = []
            xHeightList = []
            
            if self.blueLinesBox == 1:
                stroke(0, 1, 0, .25)
            else:
                stroke(0, 0, 0, .25)
            
            for i in spacerRange:
                spacer = i * xHeightTarget
        
                line((marginLBR, firstXHeightLine - spacer),
                     (pageWidth - marginLBR, firstXHeightLine - spacer)) # x-height line
                     
                line((marginLBR, firstXHeightLine - spacer - xHeightTarget),
                     (pageWidth - marginLBR, firstXHeightLine - spacer - xHeightTarget)) # baseline
                
                xHeightList.append(firstXHeightLine - spacer)
                baselineList.append(firstXHeightLine - spacer - xHeightTarget)
            
            return xHeightList, baselineList
        
        
        def _drawAscender(xHeightlist):
            
            stroke(0, 0, 1, 1)
            
            for xHeight in xHeightList:
                line((marginLBR, xHeight + ascenderTarget), (pageWidth - marginLBR, xHeight + ascenderTarget))
    
                         
        def _drawDescender(baselineList):
            
            stroke(1, 0, 0, 1)
            
            for baseline in baselineList:
                line((marginLBR, baseline + descenderTarget), (pageWidth - marginLBR, baseline + descenderTarget))
            
                
        xHeightList = _drawSketchLines()[0]
        baselineList = _drawSketchLines()[1]
        
        _drawHeader()
        _drawSketchLines()
        
        if self.ascenderBox == 1:
            _drawAscender(xHeightList)
        
        elif self.descenderBox ==1:
            _drawDescender(baselineList)
        
        self.refreshCanvas()

        
    def drawLetters(self):        
    
       # self.drawDescender()

        fill(0, 0, 0, 1)
        stroke(0, 0, 0, 0)

        translate(marginLBR, firstXHeightLine-xHeightTarget)

        for g in self.inputText:
            
            pen = CocoaPen(f)
            
            scale(xFactor)
            
            f[g].draw(pen)
            drawPath(pen.path)
            translate(f[g].width, 0)
            
            scale(1/xFactor)

        self.refreshCanvas()
         
                 
    def refreshCanvas(self):
        pdf = pdfImage()
        self.w.canvas.setPDFDocument(pdf)

EtchASketch()