f = CurrentFont()

yPoints = []

for g in f:
    for contour in g:
        for point in contour.points:
            yPoints.append(point.y)

print "lowest y: {}".format(min(yPoints))
print "highest y: {}".format(max(yPoints))