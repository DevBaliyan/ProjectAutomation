import fitz  # PyMuPDF

# Open the PDF
doc = fitz.open("MyPerf.pdf")

# Extract text
text = ""
l = 0
file = open("Ques.txt", 'a', encoding="utf-8")
for page in doc:
    l += 1
    file.write(page.get_text("text"))

# Print the extracted text
#print(text)
