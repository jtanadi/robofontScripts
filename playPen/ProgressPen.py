"""
Trying to figure out BasePen stuff...

Bezier division math borrowed from Alexandre Saumier Demers's BroadNibBackground

The script makes a copy of the font, decomposes each copied glyph, removes overlaps,
and breaks contours at each on-curve point. If this isn't done, the "progress" effect
doesn't work... Maybe this can be done on-the-fly with another pen?
"""

from vanilla import *
from defconAppKit.windows.baseWindow import BaseWindowController

from mojo.drawingTools import *
from mojo.canvas import Canvas
from mojo.events import addObserver, removeObserver

from fontTools.pens.basePen import BasePen
from robofab.interface.all.dialogs import Message
from lib.UI.spaceCenter.glyphSequenceEditText import GlyphSequenceEditText

import string as s

# Global variable that affects the resolution of each curve & the number of progress "steps"
SEGMENTS = 20

class ProgressPen(BasePen):
    """
    A pen draws the "progress" of each glyph.

    This pen is a subclass of the FontTools BasePen and extends it
    by accepting the desired "progress" as a parameter.
    """

    def __init__(self, glyphSet, progress):
        super(ProgressPen, self).__init__(glyphSet)
        self.progress = progress

    def _moveTo(self, (x, y)):
        moveTo((x, y))

    def _lineTo(self, (x, y)):
        x0, y0 = self._getCurrentPoint()
        points = self._getPointsOnLine(SEGMENTS, (x0, y0), (x, y))

        self.drawProgress(points)

    def _curveToOne(self, (x1, y1), (x2, y2), (x3, y3)):
        x0, y0 = self._getCurrentPoint()
        points = self._getPointsOnCurve(SEGMENTS, (x0, y0), (x1, y1), (x2, y2), (x3, y3))

        self.drawProgress(points)

    def _closePath(self):
        pass

    def _getPointsOnLine(self, n, (x0, y0), (x1, y1)):
        points = []

        for t in range(1, n):
            t = t/n

            fx = x0 + t * (x1 - x0)
            fy = y0 + t * (y1 - y0)

            points.append((fx, fy))

        points.append((x1, y1))

        return points

    def _getPointsOnCurve(self, n, (x0, y0), (x1, y1), (x2, y2), (x3, y3)):
        points = []

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

        points.append((x3, y3))

        return points

    def drawProgress(self, points):
        # Uses self.progress to determine the end of the points list
        for i in range(self.progress):
            x, y = points[i]
            lineTo((x, y))


def progressDrawGlyph(glyph, progress):
    """
    Similar to drawBot / mojo.drawingTools drawGlyph,
    but uses ProgressPen
    """
    newPath()
    pen = ProgressPen(glyph.getParent(), progress)
    glyph.draw(pen)
    drawPath()


class PreviewProgress(BaseWindowController):
    """
    GUI preview of ProgressPen result
    """

    def __init__(self):
        self.f = CurrentFont()
        self.letters = ""
        self.progress = 0
        self.scale = 0.25

        self.w = FloatingWindow((1200, 400),
                                "Preview Progress")

        self.w.inputText = GlyphSequenceEditText((10, 10, 500, 24),
                                                 self.f.naked(),
                                                 callback=self.inputTextCallback)

        self.w.facetSlider = Slider((520, 10, 250, 24),
                                    minValue=0,
                                    maxValue=SEGMENTS,
                                    value=self.progress,
                                    tickMarkCount=SEGMENTS,
                                    stopOnTickMarks=True,
                                    callback=self.progressSliderCallback)

        self.w.scaleSlider = Slider((800, 10, 250, 24),
                                    minValue=0,
                                    maxValue=0.5,
                                    value=self.scale,
                                    callback=self.scaleSliderCallback)

        self.w.canvas = Canvas((10, 50, -10, -10),
                               canvasSize=(1200, 350),
                               hasHorizontalScroller=False,
                               hasVerticalScroller=False,
                               delegate=self)

        self.breakGlyphCopies()

        addObserver(self, "updateFont", "fontBecameCurrent")
        self.setUpBaseWindowBehavior()

        self.w.open()

    def updateFont(self, info):
        self.f = info.get("font", None)
        self.breakGlyphCopies()

        self.w.canvas.update()

    def inputTextCallback(self, sender):
        # Making sure self.letters only contain alpha because Canvas will crash otherwise
        if not sender.get().isalpha():
            self.w.inputText.set(self.letters)

        self.letters = sender.get()

        self.w.canvas.update()

    def progressSliderCallback(self, sender):
        self.progress = int(sender.get())

        self.w.canvas.update()

    def scaleSliderCallback(self, sender):
        self.scale = sender.get()

        self.w.canvas.update()

    def windowCloseCallback(self, sender):
        removeObserver(self, "fontBecameCurrent")
        super(PreviewProgress, self).windowCloseCallback(sender)

    def breakGlyphCopies(self):
        """
        Make a copy of the current font, then decompose & remove overlaps
        from each glyph, and break contours at on-curve points.
        """
        self.fCopy = self.f.copy()

        for glyph in self.fCopy:
            if glyph.name in s.ascii_letters:

                for comp in glyph.components:
                    comp.decompose()

                glyph.removeOverlap()

                for contour in glyph:
                    for point in contour.points:
                        if point.type != "offCurve":
                            contour.breakContour(point)

    def draw(self):
        """
        This function is what Canvas calls to draw
        """

        fill(None)
        stroke(0)
        strokeWidth(4)

        translate(10, 90)
        scale(self.scale)

        for letter in self.letters:
            glyph = self.fCopy[letter]

            progressDrawGlyph(glyph, self.progress)
            translate(glyph.width, 0)

if CurrentFont() is not None:
    PreviewProgress()

else:
    Message("You need to open a font!")
