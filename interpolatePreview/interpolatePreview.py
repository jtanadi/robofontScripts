from vanilla import *
from mojo.drawingTools import *
from mojo.events import addObserver, removeObserver

f = CurrentFont()
g = CurrentGlyph()

class InterPolationPreview(object):

    def __init__(self):
        self.interValue = 0.5

        self.w = FloatingWindow((200, 200))

        self.w.interValueSlider = Slider((10, 10, -10, 23),
                                         minValue=-1,
                                         maxValue=2,
                                         value=self.interValue,
                                         callback=self.interValueSliderCallback)

        self.w.closeButton = Button((10, 100, -10, 25),
                                    "Close",
                                    callback=self.closeButtonCallback)

        self.w.open()
        addObserver(self, "drawInterpolation", "drawBackground")
        addObserver(self, "drawInterpolation", "drawPreview")

    def interValueSliderCallback(self, sender):
        self.interValue = sender.get()
        g.update()

    def closeButtonCallback(self, sender):
        self.w.close()
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        f.removeLayer("temp-interpolation")
        g.update()

    def drawInterpolation(self, info):
        gFore = g.getLayer("foreground")
        gBack = g.getLayer("background")

        g.getLayer("temp-interpolation").interpolate(self.interValue, gFore, gBack)

        f.setLayerDisplay("temp-interpolation", "Stroke", 0)
        gInter = g.getLayer("temp-interpolation")

        save()
        translate(g.width, 0)
        drawGlyph(gInter)
        restore()


InterPolationPreview()