from tkinter import *
from pdf2jpg import pdf2jpg
from PIL import Image, ImageTk

import math

class MainWindow(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)        
        self.diag_container = Frame(self)        
        self.diag_container.grid(row=0, column=0)
        self.preview_container = Frame(self)        
        self.preview_container.grid(row=1, column=0)
        self.crop_container = Frame(self)        
        self.crop_container.grid(row=0, column=1, rowspan=2)

        self.open_crop_button = Button(self.diag_container, text='Open Files to Crop', bg='lightblue')
        self.open_crop_button.grid(row=0, column=0)
        self.save_crop_button = Button(self.diag_container, text='Save Cropped Photos', bg='lightblue')
        self.save_crop_button.grid(row=0, column=1) 

        pdf2jpg.convert_pdf2jpg("C:/Users/joswar/Downloads/pdf_test.pdf", "C:/Users/joswar/Downloads/", dpi=300, pages="1")                
        im = Image.open("C:/Users/joswar/Downloads/sample.pdf_dir/0_sample.pdf.jpg")
        width, height = im.size
        print(width, height)
        new_width = math.ceil(width / 5)
        new_height = math.ceil(height / 5)
        print(new_width, new_height)
        im = im.resize((new_width, new_height))
        ph = ImageTk.PhotoImage(im)
        label = Label(self.crop_container, image=ph)
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
    root.wm_geometry("800x500")
    root.title("46 Punch")
    root.mainloop()
