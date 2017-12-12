f = CurrentFont()

yPoints = []

for g in f:
    g.copyToLayer("tempCopy")
    g.decompose()

    for contour in g.contours:
        for point in contour.points:
            yPoints.append(point.y)

    g.flipLayers("tempCopy", "foreground")

f.removeLayer("tempCopy")

print "lowest y: {}".format(min(yPoints))
print "highest y: {}".format(max(yPoints))
