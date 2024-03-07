from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def save_text_to_file(text, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)

# Example usage
pdf_path = r"text.pdf"  # Replace with the path to your PDF file
output_file = "output.txt"  # File to save extracted text
text = extract_text_from_pdf(pdf_path)
save_text_to_file(text, output_file)
print("Text extracted and saved to", output_file)
