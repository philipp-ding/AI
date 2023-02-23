from PyPDF2 import PdfReader

reader = PdfReader(r"C:\Users\Phili\Downloads\p36-weizenabaum(2).pdf")
all_text=""
for page in reader.pages:
    all_text += page.extract_text()

text = all_text.split("ELIZA Script")[-1]
text = text.split("I=~ECEIVi.3D")[0]
print(text)
with open("ELIZA Script.txt", "w") as f:
    f.write(text)