from vanilla import *
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import *

cG = CurrentGlyph()

class PatternPreview(object):

    def __init__(self):
        self.heightRadio, self.heightInput, self.gridCheck = 0, 100, 0
        self.height = CurrentFont().info.unitsPerEm

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


        self.window.heightInput = EditText((30, row + 45, -10, 22),
                                           text=self.heightInput,
                                           callback=self.heightInputCallback)

        row += 75
        self.window.gridCheck = CheckBox((12, row, -10, 22),
                                         "9-grid",
                                         callback=self.gridCallback)

        row += 30
        self.window.closeButton = Button((10, row, -10, 20),
                                         "Close",
                                         callback=self.closeButtonCallback)

        addObserver(self, "drawPattern", "drawBackground")
        addObserver(self, "previewPattern", "drawPreview")

        self.setDefaults()
        self.window.open()


    def setDefaults(self):
        self.window.heightRadio.set(0)
        self.window.heightInput.enable(False)

    def heightRadioCallback(self, sender):
        self.heightRadio = sender.get()

        if self.heightRadio == 0:
            self.height = CurrentFont().info.unitsPerEm
            self.window.heightInput.enable(False)

        elif self.heightRadio == 1:
            self.height = self.heightInput
            self.window.heightInput.enable(True)

        cG.update()

    def heightInputCallback(self, sender):
        self.window.heightInput.set(sender.get().lstrip("0"))

        try:
            self.heightInput = int(sender.get())

        except ValueError:
            self.window.heightInput.set(self.heightInput)

        #self.drawPattern()

    def gridCallback(self, sender):
        self.gridCheck = sender.get()
        #self.drawPattern()

    def closeButtonCallback(self, sender):
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        self.window.close()

    def drawPattern(self, info):
        g = info.get("glyph", "")

        if self.gridCheck == 1:
            for col in range(-1, 2):
                for row in range(-1, 2):
                    if (col or row) != 0:
                        save()
                        fill(0, 0, 0, .5)
                        translate(col * g.width, row * self.height)
                        drawGlyph(g)
                        restore()

        else:
            for col in range(-1, 2):
                if col != 0:
                    save()
                    fill(0, 0, 0, .5)
                    translate(col * g.width, 0)
                    drawGlyph(g)
                    restore()

    def previewPattern(self, info):
        gg = info.get("glyph", "")

        if self.gridCheck == 1:
            for col in range(-1, 2):
                for row in range(-1, 2):
                    if (col or row) != 0:
                        save()
                        fill(0, 0, 0, 1)
                        translate(col * gg.width, row * self.height)
                        drawGlyph(gg)
                        restore()

        else:
            for col in range(-1, 2):
                if col != 0:
                    save()
                    fill(0, 0, 0, 1)
                    translate(col * gg.width, 0)
                    drawGlyph(gg)
                    restore()

PatternPreview()
