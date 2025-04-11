import json
import re

file = open("CogniteV5.txt", 'r', encoding="utf-8")
txt = file.read()
file.close()

#pattern = "(?:Licensed to mukulthuddiless3@gmail.com\nTest\s\d+\s:\s)([\s\S]*?)(?:Start Test\n)([\s\S]*?)(?=\n{2}|$)"
pattern = r"(?:Licensed to mukulthuddiless3@gmail.com\nTest\s\d+\s:\s)([\s\S]*?)(?:Start Test\n)([\s\S]*?)(?=\n{2}Licensed|$)"
matches = re.findall(pattern, txt)

text, l = "", 0

#Perfectly Separates Unit Header and Question Part. Check Matches for more info.
##Created File Using below Steps
##for match in matches:
##    text += match[0]+match[1]+"\n\n<End_Paper>\n\n"
##    l = len(match[0]+match[1])
##    print(l)
##file = open("CogniteV5_2.txt", 'w', encoding="utf-8")
##file.write(text)
##839521
##file.close()


