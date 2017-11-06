from vanilla import *
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import *
from defconAppKit.windows.baseWindow import BaseWindowController

f = CurrentFont()
UPM = f.info.unitsPerEm

class PatternPreview(BaseWindowController):
    def __init__(self):
        self.glyph = CurrentGlyph()
        self.heightRadio, self.rowOnlyCheck = 0, 0
        self.height, self.inputHeight = UPM, UPM

        self.buildUI()

    def buildUI(self):
        self.w = FloatingWindow((170, 160),
                                closable=True)

        row = 5
        self.w.heightTitle = TextBox((10, row, -10, 17),
                                     "Cell Height:")

        row += 20
        self.w.heightRadio = RadioGroup((10, row, -10, 42),
                                        ["Use font UPM", "Use custom height"],
                                        callback=self.heightRadioCallback)
        self.w.heightRadio.set(0)

        self.w.heightInput = EditText((30, row + 45, -10, 22),
                                      text=self.height,
                                      callback=self.heightInputCallback)
        self.w.heightInput.enable(False)

        row += 75
        self.w.rowOnlyCheck = CheckBox((12, row, -10, 22),
                                       "Single row only",
                                       callback=self.rowOnlyCallback)

        addObserver(self, "chageGlyph", "viewDidChangeGlyph")
        addObserver(self, "showPatternBackground", "drawBackground")
        addObserver(self, "showPatternPreview", "drawPreview")

        self.setUpBaseWindowBehavior()
        self.w.open()

    def heightRadioCallback(self, sender):
        self.heightRadio = sender.get()

        if self.heightRadio == 0:
            self.height = UPM
            self.window.heightInput.enable(False)

        elif self.heightRadio == 1:
            self.height = self.inputHeight
            self.window.heightInput.enable(True)

        self.glyph.update()

    def heightInputCallback(self, sender):
        self.window.heightInput.set(sender.get().lstrip("0"))

        try:
            self.inputHeight = int(sender.get())
            self.height = self.inputHeight
        except ValueError:
            self.window.heightInput.set(self.inputHeight)

        self.glyph.update()

    def rowOnlyCallback(self, sender):
        self.rowOnlyCheck = sender.get()
        self.glyph.update()

    def windowCloseCallback(self, sender):
        removeObserver(self, "viewDidChangeGlyph")
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        self.glyph.update()

        super(PatternPreview, self).windowCloseCallback(sender)

    def chageGlyph(self, info):
        self.glyph = info.get("glyph", "")

    def showPatternBackground(self, info):
        fill(0, 0, 0, 0.5)
        self.drawPattern()

    def showPatternPreview(self, info):
        fill(0)
        self.drawPattern()

    def drawPattern(self):
        if self.rowOnlyCheck == 0:
            rowStart, rowEnd = -1, 2
        else:
            rowStart, rowEnd = 0, 1

        for col in range(-1, 2):
            for row in range(rowStart, rowEnd):
                if (col or row) != 0:
                    save()
                    translate(col * self.glyph.width, row * self.height)
                    drawGlyph(self.glyph)
                    restore()


PatternPreview()

"""
---------------
     TO DO
---------------
+ 
"""
