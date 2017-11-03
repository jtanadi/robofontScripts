from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen

size("LetterLandscape")

print width()
print height()

f = CurrentFont()
text = "hello"
pointSize = 72
dpi = 72
currentXheight = f.info.xHeight
targetXheight = 2*dpi
xFactor = targetXheight / currentXheight



fill(0,0,0, 0.5)
stroke(0,0,0,1)

rect(.5*dpi,.5*dpi,5*dpi,2*dpi)

translate(0.5*dpi,.5*dpi)
scale(xFactor)

for g in text:
    pen = CocoaPen(f)
    f[g].draw(pen)
    drawPath(pen.path)
    translate(f[g].width, 0)
    
