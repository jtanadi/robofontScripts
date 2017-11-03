f = CurrentFont()

gList = []

for gName in f.selection:
    gList.append (f[gName])

for g in gList:
    g.leftMargin = f["n"].leftMargin
    g.mark = (.25, 0, .75, 1)
    
    
