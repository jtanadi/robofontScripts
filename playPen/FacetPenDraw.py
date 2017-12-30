"""
Trying to figure out BasePen stuff...

Bezier division math borrowed from Alexandre Saumier Demers's BroadNibBackground

This is a second test: FacetPen is divided into 3 pens:
FacetAbstractPen, FacetPreviewPen, FacetDrawPen.

FacetAbstractPen does all the calculations without doing any drawing.
FacetPreviewPen is a subclass of FacetAbstractPen and is used to preview drawings in a mojo canvas.
FacetDrawPen is a subclass of FacetAbstractPen and is used to draw glyphs with previewed facets.
"""

from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController

from mojo.drawingTools import *
from mojo.canvas import Canvas
from mojo.events import addObserver, removeObserver

# from drawBot import *
# from drawBot.ui.drawView import DrawView

from fontTools.pens.basePen import BasePen
from robofab.interface.all.dialogs import Message


class FacetAbstractPen(BasePen):
    """
    A pen that turns curves into facets. Similar to RoboFab FlattenPen.

    This pen is a subclass of the FontTools BasePen and extends it by
    accepting the number of desired segments as a parameter.

    This pen doesn't do actual drawing, but does all the calculations.
    """
    def __init__(self, glyphSet, segments):
        super(FacetAbstractPen, self).__init__(glyphSet)
        self.segments = segments
        self.moveFlag = False
        self.firstLine = True

    def _moveTo(self, (x, y)):
        self.firstPoint = (x, y)
        self.moveFlag = True
        self.firstLine = True

        self.drawSegments(self.firstPoint)


    def _lineTo(self, (x, y)):
        x0, y0 = self._getCurrentPoint()
        points = self._getPointsOnLine(self.segments, (x0, y0), (x, y))
        self.moveFlag = False

        self.drawSegments(points)
        self.firstLine = False


    def _curveToOne(self, (x1, y1), (x2, y2), (x3, y3)):
        x0, y0 = self._getCurrentPoint()
        points = self._getPointsOnCurve(self.segments, (x0, y0), (x1, y1), (x2, y2), (x3, y3))
        self.moveFlag = False

        self.drawSegments(points)
        self.firstLine = False


    def _closePath(self):
        x0, y0 = self._getCurrentPoint()
        self.moveFlag = False

        if (x0, y0) != self.firstPoint:
            points = self._getPointsOnLine(self.segments, (x0, y0), self.firstPoint)

            self.drawSegments(points)


    _endPath = _closePath


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
        raise NotImplementedError


class FacetPreviewPen(FacetAbstractPen):
    """
    Pen that lets you preview facets.
    This pen is a subclass of FacetAbstractPen and draws using drawBot.
    """
    def drawSegments(self, points):
        if self.moveFlag:
            moveTo(points)

        else:
            if self.firstLine:
                points = points[1:]

            for point in points:
                lineTo(point)


class FacetDrawPen(FacetAbstractPen):
    """
    Pen that draws & modifies glyphs.
    This pen is a subclass of FacetAbstractPen.
    """
    def __init__(self, drawingPen, glyphSet, segments):
        super(FacetDrawPen, self).__init__(glyphSet, segments)
        self.drawingPen = drawingPen

    def _closePath(self):
        x0, y0 = self._getCurrentPoint()
        print x0, y0
        print self.firstPoint
        self.moveFlag = False

        if (x0, y0) != self.firstPoint:
            points = self._getPointsOnLine(self.segments, (x0, y0), self.firstPoint)
            self.drawSegments(points)

        self.drawingPen.closePath()


    def drawSegments(self, points):
        if self.moveFlag:
            self.drawingPen.moveTo(points)

        else:
            if self.firstLine:
                points = points[1:]

            for point in points:
                self.drawingPen.lineTo(point)


def facetPreviewGlyph(glyph, facets):
    """
    Similar to drawBot / mojo.drawingTools drawGlyph,
    but uses FacetPen
    """
    newPath()
    pen = FacetPreviewPen(glyph.getParent(), facets)
    glyph.draw(pen)
    drawPath()


def facetDrawGlyph(glyph1, facets):
    f = glyph1.getParent()

    g = f.newGlyph(glyph1.name + ".alt")
    a = glyph1

    g.width = a.width

    for c in a.components:
        c.decompose()

    pen = g.getPen()
    facetPen = FacetDrawPen(pen, f, facets)

    for contour in a.contours:
        contour.draw(facetPen)


class PreviewFacet(BaseWindowController):
    """
    GUI preview of FacetPen result
    """
    def __init__(self):
        self.f = CurrentFont()
        self.letters = ""
        self.facet = 5

        self.w = FloatingWindow((1200, 600),
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

        self.w.drawButton = Button((1090, 10, 100, 24),
                                   title="Draw",
                                   callback=self.drawButtonCallback)

        # self.w.canvas = DrawView((10, 50, -10, -10))

        self.w.canvas = Canvas((10, 50, -10, -10),
                               canvasSize=(1500, 550),
                               hasHorizontalScroller=False,
                               hasVerticalScroller=False,
                               delegate=self)

        addObserver(self, "updateFont", "fontBecameCurrent")
        self.setUpBaseWindowBehavior()

        # self.updateCanvas()

        self.w.open()


    def updateCanvas(self):
        # newDrawing()
        # newPage(1200, 525)
        # self.draw()
        # pdfData = pdfImage()
        # self.w.canvas.setPDFDocument(pdfData)

        self.w.canvas.update()


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
        self.facet = int(sender.get())

        self.updateCanvas()


    def drawButtonCallback(self, sender):
        self.f.prepareUndo("nope")

        for letter in self.letters:
            facetDrawGlyph(self.f[letter], self.facet)

        self.f.performUndo()


    def windowCloseCallback(self, sender):
        removeObserver(self, "fontBecameCurrent")
        super(PreviewFacet, self).windowCloseCallback(sender)


    def draw(self):
        fill(0)
        stroke(None)

        translate(10, 140)
        scale(.4)

        for letter in self.letters:
            glyph = self.f[letter]

            # myDrawGlyph(glyph)
            facetPreviewGlyph(glyph, self.facet)

            translate(glyph.width, 0)


if CurrentFont() is not None:
    PreviewFacet()

else:
    Message("You need to open a font!")
