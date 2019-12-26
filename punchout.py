#!C:\Users\joswar\AppData\Local\Programs\Python\Python38-32\python.exe
# pdf2image requires poppler setup instructions found here: https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows

from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter import messagebox
from tkinter import *
from pdf2image import convert_from_path
from PIL import Image, ImageTk

import math
import os

class MainWindow(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        
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
        # Mouse Drag Coordinate Vars
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

        # Widgets
        self.button_container = Frame(self)        
        self.button_container.pack(side='top', fill='x', padx=10, pady=(10, 0))
        self.pdf_container = Canvas(self, width=850, height=1100)        
        self.pdf_container.pack(pady=(10, 0))
        self.pdf_image = PhotoImage(file=os.path.join(self.py_module_path, "placeholder.gif"))
        self.pdf_container.create_image(0, 0, image=self.pdf_image, anchor=NW)

        self.open_files_button = Button(self.button_container, text='Select PDFs to Crop & Save Location', command=self.open_crop_save, bg='lightblue')
        self.open_files_button.pack(side='left', fill='x', expand=1)

    def open_crop_save(self):
        self.image_files = []
        self.current_image = 0
        for old_file in os.listdir(self.temp_path):
            os.remove(os.path.join(self.temp_path, old_file))
        while not self.pdf_files:
            self.pdf_files = askopenfilenames(initialdir="/", filetypes =(("PDF File", "*.pdf"), ("All Files","*.*")), title="Choose PDFs to Crop...")        
        for pdf in self.pdf_files:
            convert_from_path(pdf, output_folder=self.temp_path, size=(850, 1000))
        for image in os.listdir(self.temp_path):
            self.image_files.append(os.path.join(self.temp_path, image))        
        self.display_image_method()
        while not self.save_directory:
            self.save_directory = askdirectory(title="Choose Cropped Save Location")

    def display_image_method(self):
        self.image_to_display = self.image_files[self.current_image]        
        self.image_to_crop = Image.open(self.image_files[self.current_image])
        self.display_on_canvas = PhotoImage(file=self.image_to_display)
        self.pdf_container.create_image(0, 0, image=self.display_on_canvas, anchor=NW)
        self.pdf_container.bind("<Button-1>", self.drag_start)
        self.pdf_container.bind("<B1-Motion>", self.drag_end)
        self.pdf_container.bind("<ButtonRelease-1>", self.drag_complete)

    def next_current_image(self):
        if self.current_image <= len(self.image_files):
            self.current_image = self.current_image + 1

    def drag_start(self, event):
        self.left = event.x
        self.top = event.y        

    def drag_end(self, event):        
        self.right = event.x
        self.bottom = event.y        
        
    def drag_complete(self, event):
        try:
            if not self.left > self.right and not self.top > self.bottom:
                print(self.left, self.top, self.right, self.bottom)
                save_this = self.image_to_crop.crop((self.left, self.top, self.right, self.bottom))
                save_this.save(os.path.join(self.save_directory, "test.jpg"))
                self.next_current_image()
                self.display_image_method()
        except SystemError:
            pass

if __name__ == '__main__':
    root = Tk()    
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.iconbitmap(os.path.join(main.py_module_path, "box_gloves.ico"))
    root.wm_geometry("900x1165")
    root.title("46 Punch")
    root.mainloop()
