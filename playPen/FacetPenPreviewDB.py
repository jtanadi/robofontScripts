"""
Trying to figure out BasePen stuff...

This uses drawBot's DrawView (vs. mojo canvas)

Bezier division math borrowed from Alexandre Saumier Demers's BroadNibBackground
"""

from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController

from mojo.drawingTools import *
from mojo.events import addObserver, removeObserver

from fontTools.pens.basePen import BasePen
from mojo.UI import Message

from drawBot import *
from drawBot.ui.drawView import DrawView
from fontTools.pens.cocoaPen import CocoaPen


class FacetPen(BasePen):
    """
    A pen that turns curves into facets. Similar to RoboFab FlattenPen.

    This pen is a subclass of the FontTools BasePen and extends it by
    accepting the number of desired segments as a parameter.
    """

    def __init__(self, glyphSet, segments):
        super(FacetPen, self).__init__(glyphSet)
        self.segments = segments

    def _moveTo(self, (x, y)):
        self.firstPoint = (x, y)
        moveTo(self.firstPoint)

    def _lineTo(self, (x, y)):
        x0, y0 = self._getCurrentPoint()
        points = self._getPointsOnLine(self.segments, (x0, y0), (x, y))

        self.drawSegments(points)

    def _curveToOne(self, (x1, y1), (x2, y2), (x3, y3)):
        x0, y0 = self._getCurrentPoint()
        points = self._getPointsOnCurve(self.segments, (x0, y0), (x1, y1), (x2, y2), (x3, y3))

        self.drawSegments(points)

    def _closePath(self):
        x0, y0 = self._getCurrentPoint()
        if (x0, y0) != self.firstPoint:
            points = self._getPointsOnLine(self.segments, (x0, y0), self.firstPoint)

            self.drawSegments(points)

    def _getPointsOnLine(self, n, (x0, y0), (x1, y1)):
        points = [(x0, y0)]

        for t in range(1, n):
            t = t/n

            fx = x0 + t * (x1 - x0)
            fy = y0 + t * (y1 - y0)

            points.append((fx, fy))

        return points

    def _getPointsOnCurve(self, n, (x0, y0), (x1, y1), (x2, y2), (x3, y3)):
        points = [(x0, y0)]

        for t in range(1, n):
            t = t/n

            ax = x0 + t * (x1 - x0)
            ay = y0 + t * (y1 - y0)
            bx = x1 + t * (x2 - x1)
            by = y1 + t * (y2 - y1)
            cx = x2 + t * (x3 - x2)
            cy = y2 + t * (y3 - y2)
            dx = ax + t * (bx - ax)
            dy = ay + t * (by - ay)
            ex = bx + t * (cx - bx)
            ey = by + t * (cy - by)
            fx = dx + t * (ex - dx)
            fy = dy + t * (ey - dy)

            points.append((fx, fy))

        return points

    def drawSegments(self, points):
        for point in points:
            x, y = point
            lineTo((x, y))


def myDrawGlyph(glyph):
    """
    Similar to drawBot / mojo.drawingTools drawGlyph.

    Written here to test a hypothesis and as a reference
    for the facetDrawGlyph() function below.
    """
    pen = CocoaPen(glyph.getParent())
    glyph.draw(pen)
    drawPath(pen.path)

def facetDrawGlyph(glyph, facets):
    """
    Similar to drawBot / mojo.drawingTools drawGlyph,
    but uses FacetPen
    """
    newPath()
    pen = FacetPen(glyph.getParent(), facets)
    glyph.draw(pen)
    drawPath()


class PreviewFacet(BaseWindowController):
    """
    GUI preview of FacetPen result
    """

    def __init__(self):
        self.f = CurrentFont()
        self.letters = ""
        self.facet = 5

        self.w = FloatingWindow((1500, 600),
                                "Preview Facet")

        self.w.inputText = EditText((10, 10, 500, 24),
                                    text=self.letters,
                                    callback=self.inputTextCallback)

        self.w.facetSlider = Slider((520, 10, 500, 24),
                                    minValue=2,
                                    maxValue=9,
                                    value=self.facet,
                                    tickMarkCount=10,
                                    stopOnTickMarks=True,
                                    callback=self.facetSliderCallback)

        self.w.canvas = DrawView((10, 50, -10, -10))
        
        addObserver(self, "updateFont", "fontBecameCurrent")
        self.setUpBaseWindowBehavior()

        self.updateCanvas()
        self.w.open()

    def updateCanvas(self):
        newDrawing()
        newPage(1200, 330)
        self.draw()

        pdf = pdfImage()
        self.w.canvas.setPDFDocument(pdf)

    def updateFont(self, info):
        self.f = info.get("font", None)
        self.updateCanvas()

    def inputTextCallback(self, sender):
        # Making sure self.letters only contain alpha because Canvas will crash otherwise
        if not sender.get().isalpha():
            self.w.inputText.set(self.letters)

        self.letters = sender.get()

        self.updateCanvas()

    def facetSliderCallback(self, sender):
        self.facet = sender.get()
        self.updateCanvas()

    def windowCloseCallback(self, sender):
        removeObserver(self, "fontBecameCurrent")
        super(PreviewFacet, self).windowCloseCallback(sender)

    def draw(self):
        """
        This function is what Canvas calls to draw
        """

        fill(0)
        stroke(None)

        translate(10, 40)
        scale(.3)

        for letter in self.letters:
            glyph = self.f[letter]

            # myDrawGlyph(glyph)
            facetDrawGlyph(glyph, int(self.facet))

            translate(glyph.width, 0)

if CurrentFont() is not None:
    PreviewFacet()

else:
    Message("You need to open a font!")
