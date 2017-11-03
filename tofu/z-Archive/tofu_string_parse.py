inputText = "hello how are you"
tofuText = "e"
outputText = ""

print "".join(letter for letter in inputText if letter not in tofuText)
