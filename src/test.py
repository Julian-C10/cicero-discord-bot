text = "!"

if text[-1] in "!?.,":
    text = text[:-1]

print(text)