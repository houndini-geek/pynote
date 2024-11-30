
from tkinter import filedialog
from pypdf import PdfReader
from docx import Document



def pdf_reader():
    path = filedialog.askopenfilename(title='Open PDF file', filetypes=[("PDF files", "*.pdf")])
    if not path:
        return {"error": "No file selected."}
    
    reader = PdfReader(path)
  
    pdf_results = {
        "pages": 0,
        "text": "",
        "path": path,
        "error": None
    }

    try:
        pages = reader.pages
        pdf_results['pages'] = len(pages)
        
        for idx, page in enumerate(pages):
            pdf_results['text'] += page.extract_text() + "\n"
        
    except Exception as e:
        pdf_results['error'] = f"Failed to open PDF file: {e}"
    
    return pdf_results



def docx_reader():
    pass


