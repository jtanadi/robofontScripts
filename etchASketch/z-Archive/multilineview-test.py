from mojo.UI import MultiLineView
from vanilla import *
from mojo.drawingTools import *
    
f = CurrentFont()

sourcexheight = f.info.xHeight




class MyOwnSpaceCenter:

    def __init__(self, font):
        
        self._BuildUI(font)
        
        self.w.open()


    def _BuildUI(self, font):
        self.w = Window((792, 612))

        self.w.editText = EditText((10, 10, -10, 24),
                          callback=self.editTextCallback)

        self.w.lineView = MultiLineView((0, 40, -0, -0), 
                          pointSize=104,
                          lineHeight=130,
                          selectionCallback=self.lineViewSelectionCallback)
        
        #self.w.lineView.setFont(font)
        
        self.drawLines()
        
        print self.w.lineView.getDisplayStates()
   
    def drawLines(self):
        newPath()
        stroke(1,0,0)
        moveTo((36, 10))
        lineTo((100, 10))
        drawPath() 
       
            
    def editTextCallback(self, sender):
       
        letter = sender.get()
        
        glyphlist = []
        
        for glyphs in letter:
            glyphlist.append(f[glyphs])
        
        self.w.lineView.set(glyphlist)
    
    
    def lineViewSelectionCallback(self, sender):
        print sender.getSelectedGlyph()
        


MyOwnSpaceCenter(CurrentFont())