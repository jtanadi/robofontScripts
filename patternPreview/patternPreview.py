from vanilla import *
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import *

f = CurrentFont()
UPM = f.info.unitsPerEm

class PatternPreview(object):
    def __init__(self):
        self.glyph = CurrentGlyph()
        self.heightRadio, self.rowOnlyCheck = 0, 0
        self.height, self.inputHeight = UPM, UPM

        self.buildUI()

    def buildUI(self):
        self.window = FloatingWindow((170, 160),
                                     closable=False)

        row = 5
        self.window.heightTitle = TextBox((10, row, -10, 17),
                                          "Cell Height:")

        row += 20
        self.window.heightRadio = RadioGroup((10, row, -10, 42),
                                             ["Use font UPM", "Use custom height"],
                                             callback=self.heightRadioCallback)
        self.window.heightRadio.set(0)

        self.window.heightInput = EditText((30, row + 45, -10, 22),
                                           text=self.height,
                                           callback=self.heightInputCallback)
        self.window.heightInput.enable(False)

        row += 75
        self.window.rowOnlyCheck = CheckBox((12, row, -10, 22),
                                            "Single row only",
                                            callback=self.rowOnlyCallback)

        row += 30
        self.window.closeButton = Button((10, row, -10, 20),
                                         "Close",
                                         callback=self.closeButtonCallback)

        addObserver(self, "chageGlyph", "viewDidChangeGlyph")
        addObserver(self, "showPatternBackground", "drawBackground")
        addObserver(self, "showPatternPreview", "drawPreview")

        self.window.open()

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

    def closeButtonCallback(self, sender):
        removeObserver(self, "viewDidChangeGlyph")
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")

        self.glyph.update()
        self.window.close()

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
            for col in range(-1, 2):
                for row in range(-1, 2):
                    if (col or row) != 0:
                        save()
                        translate(col * self.glyph.width, row * self.height)
                        drawGlyph(self.glyph)
                        restore()

        else:
            for col in range(-1, 2):
                if col != 0:
                    save()
                    translate(col * self.glyph.width, 0)
                    drawGlyph(self.glyph)
                    restore()


PatternPreview()

"""
---------------
     TO DO
---------------
+ Switch to regular window and remove close button (add BaseWindowController)
"""
