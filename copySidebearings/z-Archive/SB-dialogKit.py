from dialogKit import *

f = CurrentFont()

gList = [f[glyphs] for glyphs in f.selection]

class SideBearing(object):

    def __init__(self):
        # f = CurrentFont()
        
        # gList = [f[glyphs] for glyphs in f.selection]
        # print gList
                
        self.w = ModalDialog((200, 200), "SB", okCallback=self.okCallback)
        self.w.textTarget = TextBox((10, 10, -10, 20), "Target")
        #self.w.radioTarget = RadioGroup((25, 30, 150, 20), ["Left SB", "Right SB"], isVertical = False, callback=self.radioTargetCallback)
        
        self.w.targetCheck1 = CheckBox((25, 30, 150, 20), ["Left SB"],callback=self.targetCheck1Callback)

        self.w.line = HorizontalLine((10, 60, -10, 1))
        
        self.w.textSource = TextBox((10, 70, -10, 20), "Source")
        # self.w.radioSource = RadioGroup((25, 90, 150, 20), ["Left SB", "Right SB"], isVertical = False, callback=self.radioSourceCallback)
        
        self.w.sourceGlyph = EditText((65, 120, 70, 22),"glyph", callback=self.editTextCallback, continuous=True)
        
        
        # self.w.button = Button((10, 155, -10, 20), "OK", callback=self.buttonCallback)
        self.w.open()

    def targetCheck1Callback(self, sender):
        global target
        target = sender.get()

    def editTextCallback(self, sender):
        global gSourceSB
        gSourceSB = f[sender.get()].leftMargin
        
    def okCallback(self, sender):
        if target == 1:
            for glyphs in gList:
                glyphs.leftMargin = gSourceSB
            
         
    # def radioTargetCallback(self, sender):
    #     if sender.get() == 0:
    #         targetSB = 1
    #         # gTargetSB = [glyphs.leftMargin for glyphs in gList]
    #         # Message(str(gTargetSB))
    #     else:
    #         targetSB = 2
    #         # gTargetSB = [glyphs.rightMargin for glyphs in gList]
        
    # def radioSourceCallback(self, sender):
    #     if sender.get() == 0:
    #         print "radio:", sender.get()
    #     elif sender.get() == 1:
    #         print "radio:", sender.get()
                     
    # def buttonCallback(self, sender):
    #     self.w.close()
SideBearing()