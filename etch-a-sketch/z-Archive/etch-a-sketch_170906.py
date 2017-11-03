import drawBot
from drawBot.ui.drawView import DrawView
from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen

f = CurrentFont()
xHeightCurrent = f.info.xHeight
descender = f.info.descender

dpi = 72 #default drawBot value
margin = .5 * dpi

class Sketcher(object):
    
    def __init__(self):
        self.text = ""
        self.xHeightTarget = 0.5*dpi
        
        self.descBox = 0
                
        self.buildUI()
        self.pageSetup()
        
        self.w.open()
        
    
    def buildUI(self):    
        
        self.w = Window((960,590),
                 #minSize = (830,500),
                 title = "Etch-A-Sketch")
        
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
        
        self.text = sender.get()
        
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
                
        
    def blueLinesCheckboxCallback(self, sender):
        
        pass

    
    def printButtonCallback(self, sender):

        drawBot.printImage()

        
    def saveButtonCallback(self, sender):
        
        # NEED TWEAKING
        def fileInfo():
            fullPath = f.path
            fileName = fullPath.split('/')[-1]
            filePath = fullPath.rstrip(fileName)
            return fileName, filePath
        
        fileInfo = fileInfo()
        name = fileInfo[0]
        path = fileInfo[1]
        
        # if name is None:
        #     name = fileInfo[0].rstrip('.ufo')
        # if path is None:
        #     path = fileInfo[1]
        # path.rstrip('/')
        # name.lstrip('/')
        fileToSave = path + '/' + name + '_SKETCH' + '.pdf'

        drawBot.saveImage(fileToSave)
        
        self.w.close()
        

    def pageSetup(self):
        drawBot.newDrawing()
        drawBot.newPage("LetterLandscape")
        
        pageWidth = drawBot.width()
        pageHeight = drawBot.height()
        
        #drawBot.fill(0,0,0, 0.5)
        drawBot.stroke(0,0,0,.5)
        drawBot.strokeWidth(0.5)
        
        #this needs major clean up
        drawBot.line((margin, pageHeight-margin), (pageWidth-dpi, pageHeight-margin)) #xHeight line
        drawBot.line((margin, pageHeight-margin-self.xHeightTarget), (pageWidth-dpi, pageHeight-margin-self.xHeightTarget)) #baseline
        
        drawBot.line((margin, pageHeight-margin-(2.5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-(2.5*self.xHeightTarget))) #xHeight line
        drawBot.line((margin, pageHeight-margin-self.xHeightTarget-(2.5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-self.xHeightTarget-(2.5*self.xHeightTarget))) #baseline
        
        drawBot.line((margin, pageHeight-margin-(5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-(5*self.xHeightTarget))) #xHeight line
        drawBot.line((margin, pageHeight-margin-self.xHeightTarget-(5*self.xHeightTarget)), (pageWidth-dpi, pageHeight-margin-self.xHeightTarget-(5*self.xHeightTarget))) #baseline

        #drawBot.rect(margin, pageHeight-margin, pageWidth-dpi, -self.xHeightTarget)
        
        pdf = drawBot.pdfImage()
        # set the pdf data in the canvas
        self.w.canvas.setPDFDocument(pdf)
        
        
    def drawLetters(self):    
    
        xFactor = self.xHeightTarget / xHeightCurrent
        descenderTarget = descender * xFactor
        
        pageWidth = drawBot.width()
        pageHeight = drawBot.height()
        
        if self.descBox == 1:
            drawBot.stroke(1,0,0, 1)
            drawBot.line((margin, pageHeight-margin-self.xHeightTarget+descenderTarget),(pageWidth-dpi, pageHeight-margin-self.xHeightTarget+descenderTarget))
        
        elif self.descBox == 0:
            drawBot.stroke(0,0,0,0)
        
        drawBot.fill(0,0,0, 1)
        drawBot.stroke(0,0,0, 0)

        drawBot.translate(margin, pageHeight-margin-self.xHeightTarget)

        drawBot.scale(xFactor)

        for g in self.text:
            pen = CocoaPen(f)
            f[g].draw(pen)
            drawBot.drawPath(pen.path)
            drawBot.translate(f[g].width, 0)
        

        pdf = drawBot.pdfImage()
        self.w.canvas.setPDFDocument(pdf)
                

Sketcher()
        
    