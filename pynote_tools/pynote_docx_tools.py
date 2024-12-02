from tkinter import filedialog,messagebox
from pdf2docx import parse
import docx
from random import randint
import logging



def docx_reader():
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



def pdf_to_docx():
    pdf_file = filedialog.askopenfilename(title='Open PDf file')
    if not pdf_file:
        return
    output_docx_file = filedialog.askdirectory(title="Select where you want to save your Docx file")
    if not output_docx_file:
        return
    
    try:
        parse(pdf_file,f'{output_docx_file}/pynote_{randint(100,400)}.docx')
    except Exception as e :
        print(f'Failed to: {e}')
