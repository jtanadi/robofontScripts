f = CurrentFont()

gList = []

for gName in f.selection:
    gList.append (f[gName])

for g in gList:
    g.leftMargin = f["o"].leftMargin
    g.mark = (.25, .75, 0, 1)
    
    
