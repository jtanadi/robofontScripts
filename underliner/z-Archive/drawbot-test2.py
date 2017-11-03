from vanilla import *
from fontTools.pens.cocoaPen import CocoaPen

f = CurrentFont()
text = "hello"
       
newPage(300,300)

fill(0,0,0, 0.5)
stroke(0,0,0,1)

translate(0,80)
scale(0.1)


for g in text:
    pen = CocoaPen(f)
    f[g].draw(pen)
    drawPath(pen.path)
    translate(f[g].width, 0)