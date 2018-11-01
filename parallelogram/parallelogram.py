from mojo.drawingTools import *
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from vanilla import FloatingWindow
from defconAppKit.windows.baseWindow import BaseWindowController

class Parallelogram(BaseWindowController):
    def __init__(self):
        self.w = FloatingWindow((150, 25), "Parallelogram")
        
        addObserver(self, "drawLines", "draw")    
        self.setUpBaseWindowBehavior()
        self.w.open()
    
    def stopButtonCB(self, sender):
        removeObserver(self, "draw")

    def collectPoints(self, glyph):
        pointsList = []
        for contour in glyph.contours:
            for point in contour.points:
                pointsList.append(point)
        
        return pointsList
        
    def findPrevOnCurvePt(self, point, pointsList):
        onCurves = []
        # Find all the non offcurves
        for pt in pointsList:
            if pt.type != "offcurve":
                onCurves.append(pt)
        # Find the matching point from a list of onCurves and
        # and return the *preceding* point
        for index, pt in enumerate(onCurves):
            if pt == point:
                return onCurves[index - 1]

    def areTheyParallel(self, line1, line2):        
        ((x0, y0), (x1, y1)) = line1
        ((x2, y2), (x3, y3)) = line2
        tolerance = .025 # arbitrary

        m1 = (y1 - y0) / (x1 - x0)
        m2 = (y3 - y2) / (x3 - x2)
        print(m1, m2)
        # instead of checking for absolute equality (m1 == m2),
        # allow for some tolerance
        return abs(m1 - m2) <= tolerance
        
    def drawLines(self, info): 
        g = info["glyph"]
        
        selectedSegment = None
        allPoints = self.collectPoints(g)
        selectedOnCurves = []
        selectedOffCurves = []
        
        # Find selected segment... is this the best way (ie. do I have to iterate?)
        for contour in g.contours:
            for segment in contour:                
                if segment.selected:
                    selectedSegment = segment
        
        if selectedSegment is None:
            return
            
        for point in selectedSegment.points:
            if point.type == "offcurve":
                selectedOffCurves.append(point)
            else:
                selectedOnCurves.append(point)
                
        pt0 = self.findPrevOnCurvePt(selectedOnCurves[0], allPoints).position
        pt1 = selectedOnCurves[0].position
        pt2 = selectedOffCurves[0].position
        pt3 = selectedOffCurves[1].position

        # if lines are parallel, lines are green
        if self.areTheyParallel((pt0, pt1), (pt2, pt3)):
            stroke(0, 1, 0, 1)
        else:
            stroke(1, 0, 0, 1)

        strokeWidth(1)
        line(pt0, pt1)
        line(pt2, pt3)
        
    def windowCloseCallback(self, sender):
        removeObserver(self, "draw")
        UpdateCurrentGlyphView()
        super(Parallelogram, self).windowCloseCallback(sender)
               
Parallelogram()