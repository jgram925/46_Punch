#!C:\Users\joswar\AppData\Local\Programs\Python\Python38-32\python.exe
# pdf2image requires poppler setup instructions found here: https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows

from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter import messagebox
from tkinter import *
from pdf2image import convert_from_path
from PIL import Image, ImageTk

import datetime
import math
import os

class MainWindow(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        
        # Datetime        
        self.datetime = datetime.datetime.now()        
        self.date = self.datetime.strftime('%m%d%H%S')
        # Project Folder & Temporary File Folder & Save Location
        py_module = os.path.abspath(__file__)
        self.py_module_path = os.path.dirname(py_module)
        self.temp_path = os.path.join(self.py_module_path, 'temp')
        self.save_directory = None
        # Image Cycling Vars
        self.pdf_files = None
        self.image_files = []
        self.current_image = 0
        self.image_to_crop = None        
        # Selection Box to Save
        self.selection_box = None
        # Crop Coordinates
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

        # Widgets
        self.config(bg='light grey')
        self.button_container = Frame(self)        
        self.button_container.pack(side='top', fill='x', padx=10, pady=(10, 0))        
        self.pdf_container = Canvas(self, width=850, height=1100)
        self.pdf_container.pack(pady=(10, 0))

        self.open_files_button = Button(self.button_container, text='Select PDFs & Save Location',
                                        command=self.open_save, font='Helvetica 12 bold', fg='white', bg='dark blue')
        self.open_files_button.pack(fill='x', expand=1)
        self.next_file_button = Button(self.button_container, text='Save Crop & Go To Next', 
                                       command=self.next_crop_image, font='Helvetica 12 bold', fg='white', bg='dark blue')
        self.next_file_button.pack(fill='x', expand=1)

        self.display_image_method()

    def open_save(self):
        self.pdf_files = None
        self.image_files = []
        self.current_image = 0
        self.image_to_crop = None        
        for old_file in os.listdir(self.temp_path):
            os.remove(os.path.join(self.temp_path, old_file))
        while not self.pdf_files:
            self.pdf_files = askopenfilenames(initialdir='/', filetypes =(('PDF File', '*.pdf'),
                                             ('All Files','*.*')), title='Choose PDFs to Crop...')        
        for pdf in self.pdf_files:
            convert_from_path(pdf, output_folder=self.temp_path, size=(850, 1100))
        for image in os.listdir(self.temp_path):
            self.image_files.append(os.path.join(self.temp_path, image))        
        self.display_image_method()
        while not self.save_directory:
            self.save_directory = askdirectory(title='Choose Cropped Save Location')

    def display_image_method(self):
        if not self.image_files or self.current_image >= len(self.image_files):
            self.image_files = []
            self.current_image = 0
            self.image_to_crop = None            
            self.pdf_image = PhotoImage(file=os.path.join(self.py_module_path, 'placeholder.gif'))
            self.pdf_container.create_image(0, 0, image=self.pdf_image, anchor=NW)
            self.pdf_container.unbind('<Button-1>')
        else: 
            self.image_to_display = self.image_files[self.current_image]        
            self.image_to_crop = Image.open(self.image_files[self.current_image])
            self.display_on_canvas = PhotoImage(file=self.image_to_display)
            self.pdf_container.create_image(0, 0, image=self.display_on_canvas, anchor=NW)
            self.pdf_container.bind('<Button-1>', self.crop_selection_box)

    def crop_selection_box(self, event):        
        if self.selection_box:
            self.pdf_container.delete(self.selection_box)
        self.left = event.x
        self.top = event.y
        self.right = event.x + 690
        self.bottom = event.y + 455
        self.selection_box = self.pdf_container.create_rectangle(self.left, self.top, self.right, self.bottom)      
        
    def next_crop_image(self):                
        save_this = self.image_to_crop.crop((self.left, self.top, self.right, self.bottom))
        filename = 'punchout-' + self.date + '.jpg'
        save_this.save(os.path.join(self.save_directory, filename))
        self.current_image = self.current_image + 1
        self.display_image_method()

if __name__ == '__main__':
    root = Tk()    
    main = MainWindow(root)
    main.pack(side='top', fill='both', expand=True)
    root.iconbitmap(os.path.join(main.py_module_path, 'box_gloves.ico'))
    root.wm_geometry('900x1205')
    root.title('46 Punch')
    root.mainloop()
