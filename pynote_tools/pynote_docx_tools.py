from tkinter import filedialog
import docx



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


