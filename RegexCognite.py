with open("CogniteV5_2_Try.txt", 'r', encoding='utf-8') as file:
    data = file.read()

import re

##exp = r"/(\[.*\]\s.*\d+)\nQuestion\s\d+\n((.|\n)*?)Options:\n((?:[A-F]:\s(.*?)(?=\n|$))+)"
##mat = re.findall(exp, data)

