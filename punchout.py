#!C:\Users\joswar\AppData\Local\Programs\Python\Python38-32\python.exe
# pdf2image requires poppler setup instructions found here: https://stackoverflow.com/questions/18381713/how-to-install-poppler-on-windows
# pyGame for selecting image for punchout

from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter.messagebox import showwarning
from tkinter import *
from pdf2image import convert_from_path
from PIL import Image, ImageTk

import math
import os

class MainWindow(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        # Temp Folder
        py_module = os.path.abspath(__file__)
        py_module_path = os.path.dirname(py_module)
        self.temp_path = os.path.join(py_module_path, 'temp')
        # Placeholder Image
        image_to_display = Image.open(os.path.join(py_module_path, 'placeholder.jpg'))
        display_img_tkinter = ImageTk.PhotoImage(image_to_display)
        self.displayed_image = Label(self.preview_container, image=display_img_tkinter)
        self.displayed_image.image=display_img_tkinter
        self.displayed_image.pack()
        # Image Cycle Vars
        self.pdf_files = None
        self.image_files = []
        self.current_image = 0
        # Image Coord Vars
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

        self.diag_container = Frame(self)        
        self.diag_container.pack(side='top', fill='x', padx=10, pady=(10, 0))
        self.preview_container = Frame(self)        
        self.preview_container.pack(fill='both', pady=10)
        self.preview_container.config(bg="black")

        self.open_files_button = Button(self.diag_container, text='Open PDFs to Crop', command=self.open_crop, bg='lightblue')
        self.open_files_button.pack(side='left', fill='x', expand=1)
        self.save_files_button = Button(self.diag_container, text='Save Cropped Location', command=self.save_crop, bg='lightblue')
        self.save_files_button.pack(side='right', fill='x', expand=1)
        
    def callme(self, event):        
        self.left = event.x
        self.top = event.y

    def callyou(self, event):        
        self.right = event.x
        self.bottom = event.y        
        
    def callthis(self, event):
        print(self.left, self.top, self.right, self.bottom)
        save_this = self.image_to_display.crop((self.left, self.top, self.right, self.bottom))        
        save_this.save("C:/Users/joswar/Desktop/test.jpg")

    def next_current_image(self):
        self.current_image = self.current_image + 1

    def display_image_method(self):
        self.image_to_display = Image.open(self.image_files[self.current_image])        
        width, height = self.image_to_display.size        
        self.image_to_display = self.image_to_display.resize((math.ceil(width / 2), math.ceil(height / 2)))
        display_img_tkinter = ImageTk.PhotoImage(self.image_to_display)
        if self.displayed_image:
            self.displayed_image.destroy()
            self.displayed_image = Label(self.preview_container, image=display_img_tkinter)      
            self.displayed_image.image=display_img_tkinter
            self.displayed_image.pack()
            self.displayed_image.bind("<Button-1>", self.callme)
            self.displayed_image.bind("<B1-Motion>", self.callyou)
            self.displayed_image.bind("<ButtonRelease-1>", self.callthis)
        else:
            self.displayed_image = Label(self.preview_container, image=display_img_tkinter)
            self.displayed_image.image=display_img_tkinter
            self.displayed_image.pack()
            self.displayed_image.bind("<Button-1>", self.callme)
            self.displayed_image.bind("<B1-Motion>", self.callyou)
            self.displayed_image.bind("<ButtonRelease-1>", self.callthis)

    def open_crop(self):
        self.image_files = []
        self.current_image = 0
        for old_file in os.listdir(self.temp_path):
            os.remove(os.path.join(self.temp_path, old_file))
        self.pdf_files = askopenfilenames(initialdir="/", filetypes =(("PDF File", "*.pdf"), ("All Files","*.*")), title = "Choose PDFs to Crop...")
        for pdf in self.pdf_files:
            convert_from_path(pdf, output_folder=self.temp_path)
        for image in os.listdir(self.temp_path):
            self.image_files.append(os.path.join(self.temp_path, image))        
        self.display_image_method()       
        
    def save_crop(self):
        self.save_directory = askdirectory()
        showwarning('Save Location', f'Files with save to: {self.save_directory}')

if __name__ == '__main__':
    root = Tk()    
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.iconbitmap("C:/Users/joswar/Projects/46_punch/box_gloves.ico")
    root.wm_geometry("900x1165")
    root.title("46 Punch")
    root.mainloop()
