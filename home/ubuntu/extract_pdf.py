import PyPDF2
import pdfplumber
import os

def extract_with_pypdf2(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            print(f"Total pages: {num_pages}")
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n\n"
        
        return text
    except Exception as e:
        print(f"Error with PyPDF2: {e}")
        return None

def extract_with_pdfplumber(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            print(f"Total pages: {num_pages}")
            
            for page_num in range(num_pages):
                page = pdf.pages[page_num]
                text += page.extract_text() + "\n\n"
        
        return text
    except Exception as e:
        print(f"Error with pdfplumber: {e}")
        return None

def main():
    pdf_path = "/home/ubuntu/upload/Phind.pdf"
    
    # Try with PyPDF2 first
    print("Attempting extraction with PyPDF2...")
    text_pypdf2 = extract_with_pypdf2(pdf_path)
    
    # If PyPDF2 fails, try with pdfplumber
    if not text_pypdf2:
        print("PyPDF2 extraction failed. Trying with pdfplumber...")
        text_pdfplumber = extract_with_pdfplumber(pdf_path)
        
        if text_pdfplumber:
            print("Successfully extracted text with pdfplumber.")
            with open("/home/ubuntu/phind_content.txt", "w", encoding="utf-8") as f:
                f.write(text_pdfplumber)
            print("Content saved to phind_content.txt")
        else:
            print("Both extraction methods failed.")
    else:
        print("Successfully extracted text with PyPDF2.")
        with open("/home/ubuntu/phind_content.txt", "w", encoding="utf-8") as f:
            f.write(text_pypdf2)
        print("Content saved to phind_content.txt")

if __name__ == "__main__":
    main()
