import string as s
import re
from vanilla import *
from mojo.UI import CurrentSpaceCenter, OpenSpaceCenter
from robofab.interface.all.dialogs import Message

def removeExtraSpaces(inputString):
    return re.sub(r"\  +", " ", inputString)

class NoTofu(object):
    def __init__(self):
        self.inputText, self.tofuText, self.outputText = "", "", ""
        self.ucCheck, self.lcCheck, self.digitCheck = 0, 0, 0
        self.punctCheck, self.copyToSCCheck = 0, 0

        self.w = FloatingWindow((450, 610),
                                "Mo Tofu Mo Problems")

        row = 10
        self.w.inputTitle = TextBox((10, row, 100, 20),
                                    "Input:")
        self.w.inputText = TextEditor((10, row+25, -10, 200),
                                      callback=self.inputTextCallback)

        row += 240
        self.w.tofuTitle = TextBox((10, row, 100, 20),
                                   "Tofu:")
        self.w.tofuText = EditText((10, row+25, -110, 50),
                                   callback=self.tofuTextCallback)

        self.w.ucCheck = CheckBox((350, row+8, 100, 20),
                                  "UC only",
                                  callback=self.ucCheckCallback)

        self.w.lcCheck = CheckBox((350, row+30, 100, 20),
                                  "lc only",
                                  callback=self.lcCheckCallback)

        self.w.digitCheck = CheckBox((350, row+52, 100, 20),
                                     "No digits",
                                     callback=self.digitCheckCallback)

        self.w.punctCheck = CheckBox((350, row+74, 100, 20),
                                     "No puncts.",
                                     callback=self.punctCheckCallback)

        row += 87
        self.w.tofuButton = Button((175, row, 100, 30),
                                   "No Mo Tofu!",
                                   callback=self.tofuButtonCallback)

        self.w.copyToSCCheck = CheckBox((75, row+5, 100, 20),
                                        "Copy to SC",
                                        callback=self.copyToSCCheckCallback)

        row += 30
        self.w.outputTitle = TextBox((10, row, 100, 20),
                                     "Output:")

        self.w.outputText = TextEditor((10, row+25, -10, 200),
                                       readOnly=True)

        self.w.open()
        self.updateFont()

    def updateFont(self):
        self.font = CurrentFont()

    def inputTextCallback(self, sender):
        self.inputText = sender.get()

    def tofuTextCallback(self, sender):
        self.tofuText = sender.get().replace(" ", "")

    def ucCheckCallback(self, sender):
        self.ucCheck = sender.get()
        self.w.lcCheck.set(0)
        self.lcCheck = 0

    def lcCheckCallback(self, sender):
        self.lcCheck = sender.get()
        self.w.ucCheck.set(0)
        self.ucCheck = 0

    def digitCheckCallback(self, sender):
        self.digitCheck = sender.get()

    def punctCheckCallback(self, sender):
        self.punctCheck = sender.get()

    def copyToSCCheckCallback(self, sender):
        self.copyToSCCheck = sender.get()

    def tofuButtonCallback(self, sender):
        self.outputText = self.inputText
        noBueno = self.tofuText

        self.updateFont()

        if self.ucCheck == 1:
            self.outputText = self.inputText.upper()
            noBueno = noBueno.upper()

        if self.lcCheck == 1:
            self.outputText = self.inputText.lower()
            noBueno = noBueno.lower()

        if self.digitCheck == 1:
            noBueno += s.digits

        if self.punctCheck == 1:
            noBueno += s.punctuation + "‘’“”«»".decode("utf-8")

        self.outputText = removeExtraSpaces("".join(letter for letter in self.outputText if letter not in noBueno))
        # outputText = outputText.translate(None, noBueno)

        self.w.outputText.set(self.outputText)

        if self.copyToSCCheck == 1 and self.outputText != "":
            try:
                OpenSpaceCenter(self.font, newWindow=False)

                sc = CurrentSpaceCenter()
                sc.setRaw(self.outputText)

            except AttributeError:
                Message("You need a font to copy to Space Center")

NoTofu()

"""
---------------
     TO DO
---------------
+ Remove formatting from input (paste as plain text)
+ Add feature to add control chars
+ Better punctuation filter
"""
