f = CurrentFont()

for g in f:    
    for layer in f.layerOrder:
        layer2Glyph = g.getLayer(layer)
        f.insertGlyph(layer2Glyph, name=g.name + "." + layer)