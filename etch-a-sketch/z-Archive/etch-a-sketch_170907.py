from drawBot import *
from drawBot.ui.drawView import DrawView
from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen

f = CurrentFont()

#Using functions as "groups"... is it worth it?

def getFontInfo():

    x = f.info.xHeight
    a = f.info.ascender
    d = f.info.descender
    
    fam = f.info.familyName
    style = f.info.styleName
    return x, a, d, fam, style


def getFileInfo():

    name = f.path.split('/')[-1]
    path = f.path.rstrip(name)
    return name, path


xHeightCurrent = getFontInfo()[0]
ascender = getFontInfo()[1]
descender = getFontInfo()[2]
fontName = getFontInfo()[3] + " " + getFontInfo()[4]
fileName = getFileInfo()[0]
filePath = getFileInfo()[1]

fileToSave = filePath + '/' + fileName + '_SKETCH' + '.pdf'


#Page Setup
dpi = 72  #default drawBot value
marginTop = 54
marginLBR = 30

pageWidth = width()
pageHeight = height()



class EtchASketch(object):
    
    def __init__(self):

        self.xHeightTarget = 0.5*dpi
        
        self.descBox = 0
                
        self.buildUI()
        self.pageSetup()
        
        self.w.open()
        
    
    def buildUI(self):    
        
        self.w = Window((960,590),
                 #minSize = (830,500),
                 title = "Etch-A-Sketch: " + fontName)
        
        self.w.inputText = EditText((10, 10, 200, 22),
                          "",
                          callback = self.inputTextCallback)
        
        self.w.xHeightText = TextBox((10, 48, 200, 17),
                             "x-Height")
        
        self.w.xHeightSlider = Slider((15, 70, 190, 23),
                               minValue = 0.5,
                               maxValue = 2,
                               value = self.xHeightTarget/dpi,
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
                                                              
        self.w.blueLinesCheckbox = CheckBox((10, -30, 150, 22),
                                  "Non-photo blue lines",
                                  callback = self.blueLinesCheckboxCallback)
        
        self.w.canvas = DrawView((220, 10, -10, -10))
        

    def inputTextCallback(self, sender):
        
        self.inputText = str(sender.get())
        #print type(self.inputText)
        
        self.pageSetup()
        self.drawLetters()
        
        
    def xHeightSliderCallback(self, sender):
        
        self.xHeightTarget = sender.get()*dpi
        
        self.pageSetup()
        self.drawLetters()
    
    
    def ascenderCheckboxCallback(self, sender):
        
        pass

    
    def descenderCheckboxCallback(self, sender):
        
        self.descBox = sender.get()
        
        self.drawDescender()
        self.refreshCanvas()
                
        
    def blueLinesCheckboxCallback(self, sender):
        
        pass

    
    def printButtonCallback(self, sender):

        printImage()

        
    def saveButtonCallback(self, sender):
        
        # NEED TWEAKING
        
        saveImage(fileToSave)
        
        self.w.close()
        

    def pageSetup(self):
        newDrawing()
        newPage("LetterLandscape")
        
        #Header
        stroke(0,0,0,1)
        strokeWidth(0.5)
        
        #pageInfo = fontName + date + time
        font("VulfMono-Light")
        fontSize(8)
        text(fontName, (marginLBR, pageHeight-27))
        line((marginLBR, pageHeight-40.5), (pageWidth-marginLBR, pageHeight-40.5))
        
        
        
        #sketch lines
        
        stroke(0,0,0,.25)
        
        
        
        #line((marginLBR, pageHeight-marginTop), (pageWidth-marginLBR, pageHeight-marginTop))
        
        #this needs major clean up
        # line((margin, pageHeight-margin), (pageWidth-dpi, pageHeight-margin)) #xHeight line
        # line((margin, pageHeight-margin-self.xHeightTarget), (pageWidth-dpi, pageHeight-margin-self.xHeightTarget)) #baseline
        
        # line((margin, pageHeight-margin-(2.5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-(2.5*self.xHeightTarget))) #xHeight line
        # line((margin, pageHeight-margin-self.xHeightTarget-(2.5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-self.xHeightTarget-(2.5*self.xHeightTarget))) #baseline
        
        # line((margin, pageHeight-margin-(5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-(5*self.xHeightTarget))) #xHeight line
        # line((margin, pageHeight-margin-self.xHeightTarget-(5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-self.xHeightTarget-(5*self.xHeightTarget))) #baseline
        
        self.refreshCanvas()
        
        
    def drawLetters(self):    
    
        xFactor = self.xHeightTarget / xHeightCurrent
        
        self.drawDescender()
        
        fill(0,0,0, 1)
        stroke(0,0,0, 0)

        translate(margin, pageHeight-margin-self.xHeightTarget)

        for g in self.inputText:
            scale(xFactor)
            pen = CocoaPen(f)
            f[g].draw(pen)
            drawPath(pen.path)
            translate(f[g].width, 0)
            scale(1/xFactor)
            
            
            # if g == " ":
            #     print f["space"].unicode
            #     translate(f["space"].width, 0)
            # else:
            #     print f[g].name
            #     scale(xFactor)
            #     pen = CocoaPen(f)
            #     f[g].draw(pen)
            #     drawPath(pen.path)
            #     translate(f[g].width, 0)
            #     scale(1/xFactor)
        
        self.refreshCanvas()
         
                
    def drawDescender(self):
        xFactor = self.xHeightTarget / xHeightCurrent
        descenderTarget = descender * xFactor
        
        if self.descBox == 1:
            
            stroke(1,0,0, 1)
            line((margin, pageHeight-margin-self.xHeightTarget+descenderTarget),
                        (pageWidth-dpi, pageHeight-margin-self.xHeightTarget+descenderTarget))
            
            
            
        elif self.descBox == 0:
            stroke(0,0,0,0)
            line((0,0),(0,0))
            
            
            
            
        
    def refreshCanvas(self):
        pdf = pdfImage()
        self.w.canvas.setPDFDocument(pdf)

EtchASketch()
        
    