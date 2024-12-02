import pyautogui as pyauto
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from docx2pdf import convert
from random import randint


def docx_to_pdf():
    docx_file = filedialog.askopenfilename(title='Open docx file to be converted in PDF file',
    filetypes=[("Docx files", "*.docx")]
    )       

    if not docx_file:
        return print('File not selected')
    
    output_pdf_file = filedialog.askdirectory(title='Select where you want to save your PDF file')
    if not output_pdf_file:
        return
    try:
  
     messagebox.showinfo(title='Converting',message='Please wait while your file is being converted...')
     convert(docx_file,f"{output_pdf_file}/pynote-{randint(100,400)}.pdf")
     print('Docx file converted to PDF. Success !')
     messagebox.showinfo(title="PDF file saved", message='Your file has been converted to PDF')
    except Exception as e:
       print(f"Failed to convert: {e}")
       messagebox.showerror(title="Error saving PDF file", message=f"Failed to convert: {e}")


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
        encrypted_file.encrypt(password,algorithm="AES-256")
        
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



def decrypt_pdf_file():
    file_path = filedialog.askopenfilename(
        title='Open PDF file to be Decrypted',
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_path:
        return

    # Open the PDF and check if it is encrypted
    file = PdfReader(file_path)

    if file.is_encrypted:
        # Ask for the decryption password
        password = pyauto.password('Enter password to decrypt the PDF:')
        
        if not password:
            pyauto.alert("No password provided. Decryption canceled.")
            return
        
        try:
            # Try to decrypt the PDF file with the provided password
            file.decrypt(password)
            
            # If decryption was successful, we can proceed
            writer = PdfWriter()

            # Add all pages to the writer after decryption
            for page in file.pages:
                writer.add_page(page)

            # Ask the user where to save the decrypted file
            decrypted_file_path = filedialog.asksaveasfilename(
                title="Save decrypted PDF file",
                defaultextension='.pdf',
                initialfile='decrypted_file.pdf'
            )

            if decrypted_file_path:
                with open(decrypted_file_path, 'wb') as f:
                    writer.write(f)
                pyauto.alert("Decrypted PDF file saved!")
                print("Decrypted PDF file saved!")
            else:
                pyauto.alert("Error: No file path provided for saving.")
                print("Error: No file path provided.")

        except Exception as e:
            # If the password is incorrect, handle the error gracefully
            pyauto.alert(f"Incorrect password! Unable to decrypt the file.{e}")
            print("Incorrect password!")
        
        except Exception as e:
            # Any other errors
            pyauto.alert(f"Failed to decrypt the file. Error: {str(e)}")
            print(f"Error during decryption: {e}")
    else:
        pyauto.alert("The PDF is not encrypted.")
        print("File is not encrypted.")

