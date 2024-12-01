
import pyautogui as pyauto
from tkinter import filedialog
from pypdf import PdfReader, PdfWriter
from pypdf.errors import FileNotDecryptedError


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


def encrypt_pdf_file():
    file_path = filedialog.askopenfilename(
     title='Open PDF file to be Encrypted',
     filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    # Check if the PDF is already encrypted
    reader = PdfReader(file_path)
    if reader.is_encrypted:
        pyauto.alert("This PDF is already encrypted. Please select a different file.")
        print("This PDF is already encrypted.")
        return

    encrypted_file = PdfWriter()

    # Add all pages to the writer first
    for idx in range(len(reader.pages)):
        page = reader.pages[idx]
        encrypted_file.add_page(page)

    # Password handling
    while True:
        password = pyauto.password('Enter password:')
        
        if password == "None":
            choice = pyauto.confirm('Do you want to cancel the encryption?', buttons=['Continue', 'Cancel'])
            if choice == 'Cancel':
                pyauto.alert('Action canceled by the user.')
                return
        elif not password.strip():
            pyauto.alert('Invalid password. Please try again.')
            continue
        
        # Encrypt the file
        encrypted_file.encrypt(password)
        
        # Ask to save the encrypted file with a default filename and extension
        encrypted_file_path = filedialog.asksaveasfilename(
            title="Save encrypted PDF file",
            defaultextension='.pdf',
            initialfile='my_encrypted_file.pdf'  # Default filename shown in the file dialog
        )
        
        if encrypted_file_path:
            with open(encrypted_file_path, 'wb') as f:
                encrypted_file.write(f)
            pyauto.alert("Encrypted PDF file saved!")
            print("Encrypted PDF file saved!")
        else:
            pyauto.alert("Error: No file path provided.")
            print('Error: No file path provided.')
        break




