from mojo.UI import SelectGlyph

f = CurrentFont()

gList = []

gSource = SelectGlyph(f, "Pick one", "left SB")
print gSource

for gName in f.selection:
    gList.append (f[gName])

for gDest in gList:
    gDest.leftMargin = gSource.leftMargin
    gDest.mark = (.25, 0, .75, 1)