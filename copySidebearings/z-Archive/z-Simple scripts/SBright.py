from mojo.UI import SelectGlyph

f = CurrentFont()

gList = []

gSource = SelectGlyph(f, "Pick one", "right SB")
print gSource

for gName in f.selection:
    gList.append (f[gName])

for gDest in gList:
    gDest.rightMargin = gSource.rightMargin
    gDest.mark = (.25, .75, 0, 1)