from vanilla import *
from drawBot import *
from drawBot.ui.drawView import DrawView
from fontTools.pens.cocoaPen import CocoaPen
from numpy import arange
from lib.UI.spaceCenter.glyphSequenceEditText import GlyphSequenceEditText
from datetime import datetime
import re
from robofab.interface.all.dialogs import Message

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
    fontName = "Font Name"
    xHeightCurrent = 500
    ascender = 250
    descender = -250

# Initial values
ppi = 72  # default drawBot value
marginTop = 54
marginLBR = 30

# Have to define these instead of using width() and height(), otherwise it doesn't work the first time script is run
pageWidth = 792
pageHeight = 612


def calculateMetrics(xHeightDrawing):

    xFactor = xHeightDrawing / xHeightCurrent
    ascenderTarget = ascender * xFactor
    descenderTarget = descender * xFactor

    return xFactor, ascenderTarget, descenderTarget


class EtchASketch(object):
    
    def __init__(self):
        
        self.ascender = ascender
        self.descender = descender
        fontRef = 0
        self.xHeightDrawing = 0.5 * ppi
        inputText = ""
        ascenderBox = descenderBox = blueLinesBox = grayLettersBox = 0
        self.newFontName = "New Font"
        
        # Instantiate Drawing class (as "drawing") & pass the following variables
        # The value of each variable is updated through UI interactions
        self.drawing = Drawing(fontName, fontRef, self.newFontName, inputText, self.xHeightDrawing,
                               ascenderBox, descenderBox, blueLinesBox, grayLettersBox)
        
        self.buildUI()
        self.refreshCanvas()
        self.w.open()
        
    
    def buildUI(self):    
        x = 10
        xText = 8
        row1 = 10
        row2 = 78
        row3 = 165
        row4 = 250
        
        self.w = Window((960,590),
                 minSize = (830,500),
                 title = "Etch-A-Sketch: " + fontName)
         
        self.w.fontNameText = EditText((x, row1, 150, 22),
                              fontName,
                              callback = self.fontNameTextCallback)
        
        self.w.newFontNameText = EditText((x, row1, 150, 22),
                                 self.newFontName,
                                 callback = self.newFontNameTextCallback)
        
        self.w.newFontNameText.show(False)                                 
                              
        self.w.fontRef = CheckBox((x+160, row1, 40, 22),
                         "Ref",
                         callback = self.fontRefCallback)                                  
                                  
        self.w.xHeightText = TextBox((xText, row2, 200, 17),
                             "x-Height (in.)")
        
        self.w.xHeightSlider = Slider((x+2, row2+22, 194, 23),
                               minValue = 0.5,
                               maxValue = 2,
                               value = self.xHeightDrawing / ppi,
                               tickMarkCount = 7,
                               stopOnTickMarks = True,
                               callback = self.xHeightSliderCallback)
                               
        self.w.xHeightMinVal = TextBox((xText, row2+48, 50, 17),
                               "0.5")
                               
        self.w.xHeightMidVal = TextBox((xText+85, row2+48, 50, 17),
                               "1.25")                               
        
        self.w.xHeightMaxVal = TextBox((xText+177, row2+48, 50, 17),
                               "2.0")
        
        self.w.guidesText = TextBox((xText, row3, 100, 17),
                            "Guides")
                                                          
        self.w.ascenderCheckbox = CheckBox((x, row3+20, 100, 22),
                                  "Ascender",
                                  callback = self.ascenderCheckboxCallback)
        
        self.w.ascenderText = EditText((x+100, row3+20, 50, 22),
                              ascender,
                              callback = self.ascenderTextCallback)        
                                          
        self.w.descenderCheckbox = CheckBox((x, row3+45, 100, 22),
                                   "Descender",
                                   callback = self.descenderCheckboxCallback)
        
        self.w.descenderText = EditText((x+100, row3+45, 50, 22),
                               descender,
                               callback = self.descenderTextCallback)
        
        self.w.extrasText = TextBox((xText, row4, 100, 17),
                            "Extras")
        
        self.w.blueLinesCheckbox = CheckBox((x, row4+20, 150, 22),
                                   "Non-photo blue lines",
                                   callback = self.blueLinesCheckboxCallback)
                                   
        self.w.grayLettersCheckbox = CheckBox((x, row4+42, 150, 22),
                                   "Gray letters",
                                   callback = self.grayLettersCheckboxCallback)
                                  
        self.w.printButton = SquareButton((x, 430, 200, -10),
                            "Print!\n(cmd + p)",
                            callback = self.printButtonCallback)
                            
        self.w.printButton.bind('p', ["command"])
         
        self.w.canvas = DrawView((220, 10, -10, -10))
        
        if f is not None:
            self.w.fontNameText.enable(False)
            
            self.w.inputText = GlyphSequenceEditText((x, row1+30, 200, 22),
                               f.naked(),
                               callback = self.inputTextCallback)
            
            self.w.ascenderText.enable(False)
            self.w.descenderText.enable(False)
                                           
            self.w.saveButton = SquareButton((x, 370, 200, 50),
                                "Save PDF!",
                                callback = self.saveButtonCallback)
                                
        else:
            self.w.fontRef.enable(False)
            self.w.inputText = EditText((x, 40, 200, 22),
                               "No open font") 
                                                 
            self.w.inputText.enable(False)
            self.w.grayLettersCheckbox.enable(False)
            
        
    def fontNameTextCallback(self, sender):
        
        self.drawing.fontName = str(sender.get())
        self.w.setTitle("Etch-A-Sketch: " + self.drawing.fontName)
        self.refreshCanvas()
    
    
    def newFontNameTextCallback(self, sender):
        self.drawing.newFontName = str(sender.get())
        self.refreshCanvas()    
        
    def fontRefCallback(self, sender):
        
        self.drawing.fontRef = sender.get()
        
        if self.drawing.fontRef == 1:
            self.w.fontNameText.show(False)
            self.w.newFontNameText.show(True)
            
        else:
            self.w.fontNameText.show(True)
            self.w.newFontNameText.show(False)

        self.refreshCanvas()
            
            
    def inputTextCallback(self, sender):
        
        self.drawing.inputTextDrawing = sender.get()
        self.refreshCanvas()
        
        
    def xHeightSliderCallback(self, sender):
        
        calculateMetrics((sender.get() * ppi))
        self.drawing.xHeightDrawing = sender.get() * ppi     
        self.refreshCanvas()
        
    
    def ascenderCheckboxCallback(self, sender):
        
        self.drawing.ascenderBoxDrawing = sender.get()
        self.refreshCanvas()

    
    def descenderCheckboxCallback(self, sender):
                
        self.drawing.descenderBoxDrawing = sender.get()
        self.refreshCanvas()


    def ascenderTextCallback(self, sender):
       
        global ascender
        
        # Check if input is an integer; if not, input is the last ascender value
        try:
            ascender = int(sender.get())
            
        except ValueError:
            self.w.ascenderText.set(ascender)
        
        self.refreshCanvas()


    def descenderTextCallback(self, sender):
        
        global descender
        
        # Catching non-digit input except for "-"... Maybe there's a better way
        # Only allowing minus sign
        if re.match(r"-", sender.get()):
            
            # Catching non-digit input _after_ digit input (for the sneakier users...)
            if re.match(r"-(\d+)?\D+", sender.get()):
                try:
                    int(sender.get())
                except ValueError:
                    self.w.descenderText.set(descender)
            
            # Only allowing "-digits" & then converting input to negative integer
            elif re.match(r"-\d+", sender.get()):
                descender = -int(sender.get().strip("-"))
                self.refreshCanvas()
        
        # If user inputs positive integer, it will auto-negative
        elif sender.get >= 0:
            
            # Catching non-digit input _after_ "0" input (again, for those sneaks...)
            if re.match(r"0?\D+", sender.get()):
                try:
                    int(sender.get())
                except ValueError:
                    self.w.descenderText.set(descender)
            else:                    
                descender = -int(sender.get())
                self.w.descenderText.set(descender)
        
        # Any non-digit input that isn't a minus sign                             
        else:
            try:
                int(sender.get())
            except ValueError:
                self.w.descenderText.set(descender)

            
    def grayLettersCheckboxCallback(self, sender):
        
        self.drawing.grayLettersBoxDrawing = sender.get()
        self.refreshCanvas()
    
        
    def blueLinesCheckboxCallback(self, sender):
        
        self.drawing.blueLinesBoxDrawing = sender.get()
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
    
    # Values accepted from EtchASketch class
    def __init__(self, fontName, fontRef, newFontName, inputText, xHeightDrawing, ascenderBox,
                 descenderBox, blueLinesBox, grayLettersBox):
         
        # Rename the variables with "self." so they can be used in this class
        self.fontName = fontName
        self.fontRef = fontRef
        self.newFontName = newFontName
        self.inputTextDrawing = inputText
        self.xHeightDrawing = xHeightDrawing
        self.ascenderBoxDrawing = ascenderBox
        self.descenderBoxDrawing = descenderBox
        self.blueLinesBoxDrawing = blueLinesBox
        self.grayLettersBoxDrawing = grayLettersBox
        
        self.pageSetup()
        
            
    def pageSetup(self):
        
        def _calculateSketchLines():
            
            if self.xHeightDrawing / ppi >= 1.75:
                n = 1 
                spaceTop = 220
            elif self.xHeightDrawing / ppi >= 1.25:
                n = 2
                spaceTop = 130
            elif self.xHeightDrawing / ppi == 1:
                n = 3
                spaceTop = 100
            elif self.xHeightDrawing / ppi == 0.75:
                n = 4 
                spaceTop = 90
            elif self.xHeightDrawing / ppi == 0.5:
                n = 6
                spaceTop = 80
   
            spacerRange = arange(0, n * 2.5, 2.5)

            self.xHeightList = []        
            self.baselineList = []
        
            for i in spacerRange:
                spaceBetween = i * self.xHeightDrawing
                                    
                self.xHeightList.append(pageHeight- spaceTop - spaceBetween)
                self.baselineList.append(pageHeight - spaceTop - spaceBetween - self.xHeightDrawing)
                
        
        def _checkAscDesc(xHeightList, baselineList):
            
            if self.ascenderBoxDrawing and self.descenderBoxDrawing == 1:                
                _drawAscender(xHeightList, ascenderTarget)
                _drawDescender(baselineList, descenderTarget)
        
            elif self.ascenderBoxDrawing == 1:
                _drawAscender(xHeightList, ascenderTarget)
    
            elif self.descenderBoxDrawing == 1:
                _drawDescender(baselineList, descenderTarget)
                      
                           
        def _drawHeader():
    
            self.dateTime = datetime.today().strftime("%m/%d/%y – %I:%M%p")
        
            cmykFill(0, 0, 0, 1, 1)
            cmykStroke(None)
            font("VulfMono-Light", 8)
            fallbackFont("Courier")

            if self.fontRef == 0:
                nameString = self.fontName
            else:
                nameString = self.newFontName + " (Ref: %s)" % self.fontName
                
            text(nameString + " – " + self.dateTime, (marginLBR, pageHeight-27))

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
            
            
        def _drawAscender(xHeightList, ascenderTarget):
            
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
        
        
        newDrawing()
        newPage("LetterLandscape")

        ascenderTarget = calculateMetrics(self.xHeightDrawing)[1]
        descenderTarget = calculateMetrics(self.xHeightDrawing)[2]
        
        _drawHeader()
        _calculateSketchLines()
        _drawSketchLines(self.xHeightList, self.baselineList)
        _checkAscDesc(self.xHeightList, self.baselineList)
        
        
    def drawLetters(self):        
            
        xFactor = calculateMetrics(self.xHeightDrawing)[0]
        
        if self.grayLettersBoxDrawing == 1:              
            cmykFill(0, 0, 0, .15, 1)
            cmykStroke(None)
            
        else:
            cmykFill(0, 0, 0, 1, 1)
            cmykStroke(None)
  
        translate(marginLBR, self.xHeightList[0] - self.xHeightDrawing)
        
        for g in self.inputTextDrawing:
    
            pen = CocoaPen(f)
    
            scale(xFactor)
    
            f[g].draw(pen)
            drawPath(pen.path)
            translate(f[g].width, 0)
    
            scale(1/xFactor)

                 
try:
    EtchASketch()
    
except NameError:
    Message("Please install DrawBot module")

"""
---------------
     TO DO
---------------
+ Make a DrawingTools version so it's not reliant on DrawBot - (is it possible? mojo.Canvas is a pain...)
+ Input string catches could be better... 
+ Expand to have typecooker mode?
+ Allow inputText string to flow to 2nd line
+ Add Observer to update everything when CurrentFont is switched
"""
