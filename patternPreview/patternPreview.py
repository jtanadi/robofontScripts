from vanilla import *
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import *
from defconAppKit.windows.baseWindow import BaseWindowController

f = CurrentFont()
UPM = f.info.unitsPerEm

class PatternPreview(BaseWindowController):
    def __init__(self):
        self.glyph = CurrentGlyph()
        self.heightRadio, self.rowOnlyCheck, self.colOnlyCheck = 0, 0, 0
        self.height, self.inputHeight = UPM, UPM

        self.buildUI()

    def buildUI(self):
        self.w = FloatingWindow((170, 155))

        row = 6
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

        row += 77
        self.w.rowOnlyCheck = CheckBox((11, row, -10, 22),
                                       "Row only",
                                       callback=self.rowOnlyCallback)

        row += 20
        self.w.colOnlyCheck = CheckBox((11, row, -10, 22),
                                       "Column only",
                                       callback=self.colOnlyCallback)

        addObserver(self, "chageGlyph", "viewDidChangeGlyph")
        addObserver(self, "showPatternBackground", "drawBackground")
        addObserver(self, "showPatternPreview", "drawPreview")

        self.setUpBaseWindowBehavior()
        self.w.open()

    def heightRadioCallback(self, sender):
        self.heightRadio = sender.get()

        if self.heightRadio == 0:
            self.height = UPM
            self.w.heightInput.enable(False)

        elif self.heightRadio == 1:
            self.height = self.inputHeight
            self.w.heightInput.enable(True)

        self.glyph.update()

    def heightInputCallback(self, sender):
        self.w.heightInput.set(sender.get().lstrip("0"))

        try:
            self.inputHeight = int(sender.get())
            self.height = self.inputHeight

        except ValueError:
            self.w.heightInput.set(self.inputHeight)

        self.glyph.update()

    def rowOnlyCallback(self, sender):
        self.rowOnlyCheck = sender.get()

        self.colOnlyCheck = 0
        self.w.colOnlyCheck.set(0)

        self.glyph.update()

    def colOnlyCallback(self, sender):
        self.colOnlyCheck = sender.get()

        self.rowOnlyCheck = 0
        self.w.rowOnlyCheck.set(0)

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
        rows = 0
        columns = 0

        if self.rowOnlyCheck == 0:
            if self.height >= 100:
                rows = 1000 // self.height
            else:
                rows = 10

        if self.colOnlyCheck == 0:
            if self.glyph.width >= 100:
                columns = 1000 // self.glyph.width
            else:
                columns = 10

        for row in range(-rows, rows + 1):
            for col in range(-columns, columns + 1):
                if (row or col) != 0:
                    save()
                    translate(col * self.glyph.width, row * self.height)
                    drawGlyph(self.glyph)
                    restore()


PatternPreview()

"""
---------------
     TO DO
---------------
+ ?
"""
