f = CurrentFont()

gList = []

for gName in f.selection:
    gList.append (f[gName])

for g in gList:
    g.rightMargin = f["o"].rightMargin
    g.mark = (.75, .25, 0, 1)
    
    
