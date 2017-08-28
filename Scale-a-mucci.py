from robofab.interface.all.dialogs import AskString, Message

f = CurrentFont()

currentEm = f.info.ascender + -f.info.descender #Total measurement from ascender to descender

newEm = AskString("Target height (ascender to descender)", title="Scale-a-mucci")

#Returns message when input is blank
if newEm == None:
    Message("You're fired!")

else:
    try:    
        #Convert input string to integers & calculate scale
        xFactor = int(newEm) / currentEm
        
        #Decompose every glyph first (in case of component-based font)
        for glyph in f:
            glyph.decompose()

        #Scale & tans every glyph
        for glyph in f:
            glyph.width *= xFactor
            glyph.scale((xFactor))
            glyph.mark = (0.69, 0.43, 0.18, 1)
    
        #Modify vertical metrics to new dimensions    
        f.info.ascender *= xFactor
        f.info.capHeight *= xFactor
        f.info.xHeight *= xFactor
        f.info.descender *= xFactor
    
        Message("Nice tan!")

    #In case user inputs strings that can't be converted to integers
    except ValueError:
        Message("The Mooch only likes numbers!")

"""
---------------
     TO DO
---------------
+ Round results (esp. side bearings) to closest integer
+ "Scale" or move guides
+ Maybe a "custom" AskString window (through Vanilla)

"""