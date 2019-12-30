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

        # Widget Frames
        self.config(bg='white')
        self.button_container = Frame(self)
        self.button_container.pack(side='top', fill='x', padx=10, pady=(10, 0))
        self.pdf_container = Canvas(self)
        self.pdf_container.pack(fill='both', expand=True, padx=10, pady=10)
        self.pdf_container.bind("<Configure>", self.canvas_resize)
        # Widget Buttons
        self.open_files_button = Button(self.button_container, text='Select PDFs & Save Location',
                                        command=self.open_save, bg='lightblue')
        self.open_files_button.pack(fill='x', expand=1)
        self.next_file_button = Button(self.button_container, text='Save Crop & Go To Next', 
                                       command=self.next_crop_image, bg='lightblue')
        self.next_file_button.pack(fill='x', expand=1)
        # Method Calls
        self.display_image_method()        

    def canvas_resize(self, event):
        print(event.width, event.height)
        self.canvas_width = event.width
        self.canvas_height = event.height

    def open_save(self):
        self.pdf_files = None
        self.image_files = []
        self.current_image = 0
        self.image_to_crop = None
        self.delete_temp_images()
        while not self.pdf_files:
            self.pdf_files = askopenfilenames(initialdir='/', filetypes =(('PDF File', '*.pdf'),
                                             ('All Files','*.*')), title='Choose PDFs to Crop...')
        while not self.save_directory:
            self.save_directory = askdirectory(title='Choose Cropped Save Location')
        for pdf in self.pdf_files:
            convert_from_path(pdf, output_folder=self.temp_path, dpi=300)
        for image in os.listdir(self.temp_path):
            self.image_files.append(os.path.join(self.temp_path, image))
        self.display_image_method()

    def display_image_method(self):
        if not self.image_files or self.current_image >= len(self.image_files):
            self.image_files = []
            self.current_image = 0
            self.image_to_crop = None            
            self.welcome_image = PhotoImage(file=os.path.join(self.py_module_path, 'box_boxers.gif'))
            self.pdf_container.create_image(0, 0, image=self.welcome_image, anchor=NW)
            self.pdf_container.unbind('<Button-1>')
        else:
            # working on resizing image based on canvas size
            # Need to change crop selection box based on scaling
            # Crop selection box coordinates will be transposed to select unscaled image
            print(self.canvas_width)
            print(self.canvas_height)
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
        date_time = datetime.datetime.now()
        date = date_time.strftime('%m%d%y-%H%S%f')
        filename = 'punchout-' + date + '.jpg'
        save_this.save(os.path.join(self.save_directory, filename), dpi=(300, 300))
        self.current_image = self.current_image + 1
        self.display_image_method()

    def delete_temp_images(self):
        for old_file in os.listdir(self.temp_path):
            os.remove(os.path.join(self.temp_path, old_file))

if __name__ == '__main__':
    root = Tk()    
    main = MainWindow(root)
    main.pack(side='top', fill='both', expand=True)
    root.iconbitmap(os.path.join(main.py_module_path, 'box_gloves.ico'))
    root.wm_geometry('525x475')
    root.title('46 Punch')
    root.mainloop()
