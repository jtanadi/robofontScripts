"""
Trying to figure out BasePen stuff...
"""

from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import *

from mojo.drawingTools import *
from mojo.canvas import Canvas
from mojo.events import addObserver, removeObserver

from fontTools.pens.basePen import BasePen

class FacetPen(BasePen):
    """
    A pen that turns curves into facets. Similar to RoboFab FlattenPen.

    This pen is a subclass of the FontTools BasePen and extends it by
    accepting the number of desired segments as a parameter.
    """

    def __init__(self, glyphSet, segment):
        super(FacetPen, self).__init__(glyphSet)
        self.segment = segment

    def _moveTo(self, pt):
        pass
    
    def _lineTo(self, pt):
        pass
    
    def _curveToOne(self, pt1, pt2, pt3):
        pass


class PreviewFacet(BaseWindowController):
    def __init__(self):
        self.f = CurrentFont()
        self.letters = ""

        self.w = Window((800, 500),
                        "Preview Facet")

        self.w.inputText = EditText((10, 10, -10, 24),
                                    callback=self.inputTextCallback)

        self.w.canvas = Canvas((10, 50, -10, -10),
                               hasHorizontalScroller=False,
                               hasVerticalScroller=False,
                               delegate=self)

        addObserver(self, "updateFont", "fontBecameCurrent")
        self.setUpBaseWindowBehavior()

        self.w.open()

    def updateFont(self, info):
        # self.f = info.get("font", None)
        pass

    def inputTextCallback(self, sender):
        self.letters = sender.get()

        self.w.canvas.update()

    def windowCloseCallback(self, sender):
        removeObserver(self, "fontBecameCurrent")
        super(PreviewFacet, self).windowCloseCallback(sender)

    def draw(self):
        """
        This is what Canvas calls to draw
        """

        fill(0,0,0, .5)
        stroke(0,0,0, 1)
        
        translate(10, 10)
        scale(.2)

        for letter in self.letters:
            glyph = self.f[letter]

            drawGlyph(glyph)
            translate(glyph.width, 0)


PreviewFacet()