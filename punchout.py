#!C:\Users\joswar\AppData\Local\Programs\Python\Python38-32\python.exe

from tkinter import *
from pdf2jpg import pdf2jpg
from PIL import Image, ImageTk

import math

class MainWindow(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)        
        self.diag_container = Frame(self)        
        self.diag_container.pack(side='top', fill='x', expand=True, padx=10)
        self.preview_container = Frame(self)        
        self.preview_container.pack(fill='both', expand=True)
        self.crop_container = Frame(self)        
        self.crop_container.pack(side='bottom', fill='x', expand=True, padx=10)

        self.open_files_button = Button(self.diag_container, text='Open Files to Crop', bg='lightblue')
        self.open_files_button.pack(side='left', fill='x', expand=1)
        self.save_files_button = Button(self.diag_container, text='Save Cropped Photos', bg='lightblue')
        self.save_files_button.pack(side='right', fill='x', expand=1)

        self.vert_crop_button = Button(self.crop_container, text='Vertical Crop', bg='lightblue')
        self.vert_crop_button.pack(side='left', fill='x', expand=1)
        self.hori_crop_button = Button(self.crop_container, text='Horizontal Crop', bg='lightblue')
        self.hori_crop_button.pack(side='right', fill='x', expand=1) 

        pdf2jpg.convert_pdf2jpg("C:/Users/joswar/Downloads/pdf_test.pdf", "C:/Users/joswar/Downloads/", dpi=300, pages="1")                
        im = Image.open("C:/Users/joswar/Downloads/sample.pdf_dir/0_sample.pdf.jpg")
        width, height = im.size
        print(width, height)
        new_width = math.ceil(width / 5)
        new_height = math.ceil(height / 5)
        print(new_width, new_height)
        im = im.resize((new_width, new_height))
        ph = ImageTk.PhotoImage(im)
        label = Label(self.preview_container, image=ph)
        label.image=ph
        label.pack()
        

        # 4x6in = 1800x1200px # Need to divide by 5
        #v = DocViewer(self.crop_container)
        #v.pack(side="top", expand=1, fill="both")
        #v.display_file("C:/Users/joswar/Downloads/sample.pdf")

if __name__ == '__main__':
    root = Tk()    
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.iconbitmap("C:/Users/joswar/Projects/46_punch/box_gloves.ico")
    root.wm_geometry("600x800")
    root.title("46 Punch")
    root.mainloop()
