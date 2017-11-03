f = CurrentFont()

gList = []

for gName in f.selection:
    gList.append (f[gName])

for g in gList:
    g.rightMargin = f["n"].rightMargin
    g.mark = (.75, 0, 0.25, 1)
    
    
