"""
Trying to figure out BasePen stuff...

Update docstring please!
"""
from math import atan2, degrees, sqrt
import random as r
import vanilla
from defconAppKit.windows.baseWindow import BaseWindowController

from mojo.drawingTools import *
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView

from fontTools.pens.basePen import BasePen
from robofab.interface.all.dialogs import Message
from lib.UI.spaceCenter.glyphSequenceEditText import GlyphSequenceEditText

import string as s

# Global variable for max width for easy adjustment
MAXWIDTH = 100

class StrokePen(BasePen):
    """
    A pen draws the strokes of glyph.

    This pen is a subclass of the FontTools BasePen and extends it
    by accepting the desired stroke width as a parameter.
    """
    def __init__(self, glyphset, width):
        super(StrokePen, self).__init__(glyphset)
        self.width = width
        self.pointsList = []
        
    def _moveTo(self, pt):
        newPath()
        self.pointsList.append(pt)
        
    def _lineTo(self, pt):
        x0, y0 = self._getCurrentPoint()
        x, y = pt
        
        save()
        fill(None)
        stroke(0, 0, 1, .5)
        strokeWidth(self.width)

        # newPath()
        moveTo((x0, y0))
        lineTo(pt)
        drawPath()
        restore()
        
        # Or use line() instead of newPath, moveTo, lineTo, drawPath combo
        # line((x0, y0), (x, y))
        
        # Use rectangle below... still not sure why one over the other
        # angle = self.getAngle((x0, y0), (x, y))
        # distance = self.getDistance((x0, y0), (x, y))
    
        # fill(0, 0, 1, 1)    
        
        # with savedState():
        #     rotate(angle, (x0, y0))
        #     rect(x0, y0 - self.width / 2, distance, self.width)
            
        self.pointsList.append(pt)        
        
    def _curveToOne(self, pt1, pt2, pt3):
        x0, y0 = self._getCurrentPoint()
        
        save()
        fill(None)
        stroke(0, 0, 1, .5)
        strokeWidth(self.width)

        # newPath()
        moveTo((x0, y0))
        curveTo(pt1, pt2, pt3)
        drawPath()
        restore()
        
        self.pointsList.append(pt3)
        
    def _closePath(self):
        pass
        # moveTo(self.pointsList[0])
        # lineTo(self.pointsList[-1])
        # drawPath()
        # self.drawCircles()
            
    def _endPath(self):
        self.pointsList.append(self._getCurrentPoint())
        save()
        self.drawCircles()
        restore()
      
    def drawCircles(self):
        """
        Draw circle at all points in pointsList
        """

        # blendMode("multiply")
        fill(1, 0, 0, 0.25)
        stroke(None)
        
        for point in self.pointsList:
            x, y = point
            newPath()
            oval(x - self.width / 2, y - self.width / 2, self.width, self.width)

        
    def getAngle(self, pt0, pt1):
        """
        Returns angle between 2 points, in degrees
        """
        x0, y0 = pt0
        x1, y1 = pt1
        
        xDiff = x1 - x0
        yDiff = y1 - y0
        
        return degrees(atan2(yDiff, xDiff))
        
    def getDistance(self, pt0, pt1):
        """
        Returns distance between two points
        """
        x0, y0 = pt0
        x1, y1 = pt1
        
        return sqrt((x1 - x0)**2 + (y1 - y0)**2)


class SimpleWindowObserver(BaseWindowController):
    
    def __init__(self):
        self.widthValue = 55

        # create a window        
        self.w = vanilla.Window((300, 70), "Simple Observer")
        # add a button with a title and a callback
        self.w.startStopButton = vanilla.Button((10, 10, -10, 22), "Start", callback=self.startStopButtonCallback)
        
        self.w.widthSlider = vanilla.Slider((10, 40, -10, 22),
                                            value=self.widthValue,
                                            minValue=10,
                                            maxValue=MAXWIDTH,
                                            callback=self.widthSliderCallback)
        
        # setup basic windwo behavoir (this is an method from the BaseWindowController)
        self.setUpBaseWindowBehavior()
        # open the window
        self.w.open()
    
    
    def widthSliderCallback(self, sender):
        self.widthValue = sender.get()
        UpdateCurrentGlyphView()
    
    def startStopButtonCallback(self, sender):
        UpdateCurrentGlyphView()
        # button callback, check the title
        if sender.getTitle() == "Start":
            # set "Stop" as title for the button
            sender.setTitle("Stop")
            # add an observer
            addObserver(self, "draw", "draw")
            addObserver(self, "draw", "drawInactive")
        else:
            # set "Start" as title for the button
            sender.setTitle("Start")
            # remove the observser
            removeObserver(self, "draw")
            removeObserver(self, "drawInactive")           
    
    def draw(self, notification):
        # get the glyph
        glyph = notification["glyph"]
        
        newPath()
        pen = StrokePen(glyph.getParent(), self.widthValue)
        glyph.draw(pen)
        drawPath()
    
    def windowCloseCallback(self, sender):
        # this receives a notification whenever the window is closed
        # remove the observer
        removeObserver(self, "draw")
        removeObserver(self, "drawInactive")
        # and send the notification to the super
        super(SimpleWindowObserver, self).windowCloseCallback(sender)
        UpdateCurrentGlyphView()
        
    
SimpleWindowObserver()

