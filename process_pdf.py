import pdb 
import pandas as pd
import PyPDF2

# Path to the PDF file
pdf_path = r'C:/Users/lvshu/Desktop/2024/NHANES-2003-2004ExaminationVariableList.pdf'

# Extracting text from the PDF
def extract_text_from_first_page(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    first_page = pdf_reader.pages[0]
    text = first_page.extract_text()
    pdf_file.close()
    return text

# Extracted text from the first page
text = extract_text_from_first_page(pdf_path)

# Extract table headers and rows
lines = text.split('\n')
headers = ["Variable Name", "Variable Description", "Data File Name", "Data File Description", "Begin Year", "End Year", "Component", "Use Constraints"]

# Extracting rows
rows = []
for line in lines:
    if line.startswith('AUX') or line.startswith('BA') or line.startswith('BP') or line.startswith('BID') or line.startswith('BIX'):
        row = line.split()
        rows.append(row)

# Creating DataFrame
df = pd.DataFrame(rows, columns=headers)

# Save to an Excel file
pdb.set_trace()
print()
# output_path = 'NHANES_Examination_2003_2004.xlsx'
# df.to_excel(output_path, index=False)

print(f"Excel file saved to {output_path}")
