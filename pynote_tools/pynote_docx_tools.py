from tkinter import filedialog,messagebox
from pdf2docx import parse
import docx
from random import randint
import logging



def docx_reader():
    try:
     path = filedialog.askopenfilename(title='Open Docx file',filetypes=[('Docx file','.docx')])
     if not path:
        return
  
     docx_results = {
        "path": path,
        "text": ''
        }
     doc = docx.Document(path)
     for para in doc.paragraphs:
        docx_results['text'] += para.text + '\n'
     return docx_results
    
    except Exception as e:
        messagebox.showerror(title="Failed to open file", message=f"Error opening the Docx file: {e}")
        print(f'Error opening the Docx file: {e}')



def pdf_to_docx():
    pdf_file = filedialog.askopenfilename(title='Open PDf file')
    if not pdf_file:
        return
    output_docx_file = filedialog.askdirectory(title="Select where you want to save your Docx file")
    if not output_docx_file:
        return
    
    try:
        parse(pdf_file,f'{output_docx_file}/pynote_{randint(100,400)}.docx')
        messagebox.showinfo(title='PDF is converting', message='Hold tigh ! the convertion might take some time')
        print(f'Hold tigh ! the convertion might take some time')
    except Exception as e :
        messagebox.showerror(title='Convertion failed', message=f'Failed to convert PDF to Docx: {e}')
        print(f'Failed to convert PDF to Docx: {e}')
