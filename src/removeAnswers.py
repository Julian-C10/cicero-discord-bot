def clipped(line):
    newLine = ""
    for c in line:
        newLine += c
        if c == "=":
            break
    newLine += "\n"
    return newLine

fileName = "sententiae-blank.txt"

with open(fileName, "r", encoding='utf8') as file:
    text = file.read()

text = text.split('\n')
newText = []
shouldSkip = False
for i in range (0, len(text)):
    if shouldSkip:
        shouldSkip = False
        continue
    if text[i].isnumeric():
        newText.append(text[i] + clipped(text[i + 1]))
        shouldSkip = True
    else:
        newText.append(f" {clipped(text[i])}")
    
text = "\n".join(newText)

with open(fileName, "w", encoding='utf8') as file:
    file.write(text)