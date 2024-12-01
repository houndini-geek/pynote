import os
from tkinter import *
from tkinter import filedialog, messagebox
from pynote_tools import pdf_reader, encrypt_pdf_file, decrypt_pdf_file
import pandas

path = None
# Get the user's home directory dynamically
home_dir = os.path.expanduser("~")
recent_file_path = os.path.join(home_dir, "recent-files.txt")



root = Tk()

# Function to retrieve recent files from a text file
def get_recent_files():
    try:
        with open(recent_file_path, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def get_file_size(path=None):
    if not path:
        return
    file_info = os.stat(path)
    file_size_bytes = file_info.st_size
    return file_size_bytes


# Function to save the recent file path
def save_to_recent_files(path):
    recent_files = get_recent_files()
    if path not in recent_files:
        recent_files.insert(0, path)
        with open(recent_file_path, "w") as file:
            file.write("\n".join(recent_files[:10]))  # Limit to 10 recent files

# Function to dynamically update recent files menu
def update_recent_menu():
    recent_files = get_recent_files()
    recent_menu.delete(0, END)
    if recent_files:
        for file_path in recent_files:
            recent_menu.add_command(label=file_path, command=lambda path=file_path: open_file(path))
    else:
        recent_menu.add_command(label="No recent files")




def new_file():
    global path 
    path = None
    textarea.delete("1.0", END)


def open_file(recent_path=None):
     global path 
     path = recent_path
     if not path:
      path = filedialog.askopenfilename(
            title="Open file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
     if path:
      try:
         file_size = get_file_size(path) / 1024
         root.title(f"Pynote: {path}:  File size: {file_size:.2f} KB")
         with open(path, 'r') as file:
                content = file.read()
                textarea.delete("1.0", END)
                textarea.insert("1.0", content)
         save_to_recent_files(path)
      except UnicodeDecodeError:
        messagebox.showerror("Error", "File type not supported.")
       
      except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
       
      except PermissionError:
        messagebox.showerror("Error", "Permission denied.")
     
      except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")



def save_file():
    global path
    content = textarea.get("1.0", END)
    try:
        if not path:
            path = filedialog.asksaveasfilename(
                title='Save file',
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
        if path:
            with open(path, 'w') as file:
                file.write(content.strip())
            root.title(f"Pynote: {path}")
    except Exception as e:
        messagebox.showwarning("File not saved", f"An error occurred: {e}")

def save_as_file():
    global path
    try:
        path = filedialog.asksaveasfilename(
            title='Save file as',
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            with open(path, 'w') as file:
                content = textarea.get("1.0", END)
                file.write(content.strip())
            root.title(f"Pynote: {path}")
    except Exception as e:
        messagebox.showwarning("File not saved", f"An error occurred: {e}")

def confirm_exit():
    if messagebox.askyesno("Exit", "Do you want to save changes before exiting?"):
        save_file()
    root.destroy()


def pdf_reader_handler():
    pdf_data = pdf_reader()
    file_size = get_file_size(pdf_data['path']) / 1024
    if pdf_data.get('error'):
          messagebox.showerror("Error", pdf_data["error"])
    else:
        textarea.delete("1.0", END)
        textarea.insert("1.0", pdf_data["text"])
        root.title(f"Pynote - {pdf_data['path']} -File size: {file_size:.2f} KB  pages: {pdf_data['pages']}")

# def docx_reader_handler():
#     results = docx_reader()
#     file_size = get_file_size(results['path']) / 1024
#     root.title(f"Pynote: {results['path']}:  File size: {file_size:.2f} KB")
#     textarea.insert('0.1',results['text'])

    

root.title("Pynote")
root.geometry("800x540")
# root.resizable(width=False, height=False)

# Create menu 
menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0, bg='#001524', foreground='#ffffff',font=('Arial Narrow', 12))
file_menu.add_command(label='New file', command=new_file)
file_menu.add_command(label='Open file', command=open_file)
file_menu.add_cascade(label="Recent Files", menu=Menu(file_menu, tearoff=0, font=('Arial Narrow', 12),bg='#001524', foreground='#ffffff', postcommand=update_recent_menu))
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Save as...', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=confirm_exit)
menu_bar.add_cascade(label='File', menu=file_menu)
recent_menu = file_menu.children["!menu"]

# Tools menu
tools_menu = Menu(menu_bar, tearoff=0, bg='#001524', foreground='#ffffff', font=('Arial Narrow', 12))
menu_bar.add_cascade(label='Tools', menu=tools_menu)


# Adding options to PDF Tool submenu
pdf_menu = Menu(tools_menu, tearoff=0, bg='#001524', foreground='#ffffff', font=('Arial Narrow', 12))
pdf_menu.add_command(label='Open PDF File', command=pdf_reader_handler)
pdf_menu.add_command(label='Encrypt PDF File',command=encrypt_pdf_file)
pdf_menu.add_command(label='Decrypt PDF File',command=decrypt_pdf_file)

docx_menu = Menu(tools_menu, tearoff=0, bg='#001524', foreground='#ffffff', font=('Arial Narrow', 12))
docx_menu.add_command(label='Open Docx file')
# PDF Tool submenu inside Tools menu
tools_menu.add_cascade(label='PDF Tool', menu=pdf_menu)
tools_menu.add_cascade(label='Docx Tool', menu=docx_menu)

# Scrollbar setup
frame = Frame(root)
frame.pack(expand=True, fill='both')

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

textarea = Text(frame, wrap=WORD, yscrollcommand=scrollbar.set)
textarea.config(bg="#020a11", foreground='#F1F1F1',
                 font=('Arial Baltic', 12),
                 insertbackground='#C1C1C1',padx=4,pady=4)
textarea.pack(expand=True, fill='both',side='top')

scrollbar.config(command=textarea.yview)

root.config(menu=menu_bar)
root.mainloop()
