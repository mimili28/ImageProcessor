import tkinter as tk
import cv2
from tkinter import Frame, Tk, BOTH, Text, Menu, END, filedialog, Label, Button
from PIL import ImageTk, Image
import numpy as np
import os
import filters

class ImageProcessor(Frame):
    """App to manipulate an image by adding filters, 
    face detection, cropping and rotation.
    Also and Undo button to reverse actions.
    It uses OpenCV image format and ImageTk from Pillow.
    Arguments:
        Frame {[type]} -- [description]
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent        
        self.initUI()
        
    # Initiates the UI 
    def initUI(self):
        """[summary]
        """
        self.parent.title("Image Processor")
        self.pack(fill=BOTH, expand=1)

        filebar = Menu(self.parent)
        self.parent.config(menu=filebar)
      
        fileMenu = Menu(filebar)
        filebar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.open_img)
        fileMenu.add_command(label="Save", command =self.save_img)
        fileMenu.add_command(label="Quit", command =self.exitProgram)

        editMenu = Menu(filebar)
        filebar.add_cascade(label= "Edit", menu= editMenu)
        editMenu.add_command(label="Undo", command = self.undo)

        imageMenu = Menu(filebar)
        filebar.add_cascade(label= "Image", menu= imageMenu)
        imageMenu.add_command(label= "Rotate Right", command= self.rotate_right_img)
        imageMenu.add_command(label= "Rotate Left", command= self.rotate_left_img)
        imageMenu.add_command(label= "Crop 4:3", command= self.crop_img)
        imageMenu.add_command(label= "Face detection", command= self.face_detect)

        filtersMenu = Menu(filebar)
        filebar.add_cascade(label= "Filters", menu= filtersMenu)
        filtersMenu.add_command(label= "Dither", command= self.call_filters_ditter)
        filtersMenu.add_command(label= "Gray Scale", command= self.call_convert_grayscale)
        filtersMenu.add_command(label= "Primary", command= self.call_convert_primary)

        filebar.add_cascade(label="Original image", command=self.show_original_img)


        self.btn = Button(root, text = 'Crop faces', command = self.crop_face)
        self.btn.pack_forget()

        self.panel = Label(root)
        self.panel.place(relx=.5, rely=.5, anchor="c")
        
        
        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

        self.states=[]

    # Method to undo an action applied to an image
    def undo(self):
        """[summary]
        """
        self.cv2img = self.states[-2]
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image = image)
        self.panel.image = image
        del self.states[-1]


    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    # Opens an image and displays it on the panel
    def open_img(self):
        """[summary]
        """
        self.cv2img = cv2.imread(self.openfn())
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)

        height_original = int(self.cv2img.shape[0])
        scale_percent = 500/height_original 
        width_new = int(self.cv2img.shape[1] * scale_percent)
        height_new = int(self.cv2img.shape[0] * scale_percent)
        dim = (width_new, height_new)
        self.cv2img = cv2.resize(self.cv2img,dim, interpolation = cv2.INTER_AREA)
        self.original = self.cv2img.copy()
        # Converts image from OpenCV to Pil Image
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
    
        self.panel.configure(image = image)
        self.panel.image = image
        self.states.append(self.cv2img)
        
    # Shows original image
    def show_original_img(self):
        """[summary]
        """
        self.cv2img = self.original
        image = Image.fromarray(self.cv2img)
        image = ImageTk.PhotoImage(image)
        self.panel.configure(image = image)
        self.panel.image = image
        
    # Rotates the image 90 degrees clockwise
    def rotate_right_img(self):
        """[summary]
        """
        self.cv2img = cv2.rotate(self.cv2img, cv2.ROTATE_90_CLOCKWISE)
        rotated = Image.fromarray(self.cv2img)
        rotated = ImageTk.PhotoImage(rotated)
        self.panel.configure(image = rotated)
        self.panel.image = rotated
        self.states.append(self.cv2img)
        

    def rotate_left_img(self):
        """[summary]
        """
        self.cv2img = cv2.rotate(self.cv2img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rotated = Image.fromarray(self.cv2img)
        rotated = ImageTk.PhotoImage(rotated)
        self.panel.configure(image = rotated)
        self.panel.image = rotated
        self.states.append(self.cv2img)

    def call_filters_ditter(self):
        """[summary]
        """
        image = Image.fromarray(self.cv2img)
        im = filters.convert_dithering(image)
        img = ImageTk.PhotoImage(im)
        self.panel.configure(image = img)
        self.panel.image = img
        # # Convert RGB to BGR 
        self.cv2img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        self.cv2img = self.cv2img[:, :, ::-1]
        self.states.append(self.cv2img)
        
    def call_convert_grayscale(self):
        """[summary]
        """
        image = Image.fromarray(self.cv2img)
        im = filters.convert_grayscale(image)
        img = ImageTk.PhotoImage(im)
        self.panel.configure(image = img)
        self.panel.image = img
        # # Convert RGB to BGR 
        self.cv2img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        self.cv2img = self.cv2img[:, :, ::-1]
        self.states.append(self.cv2img)
        
    def call_convert_primary(self):
        """[summary]
        """
        image = Image.fromarray(self.cv2img)
        im = filters.convert_primary(image)
        img = ImageTk.PhotoImage(im)
        self.panel.configure(image = img)
        self.panel.image = img
        # # Convert RGB to BGR 
        self.cv2img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        self.cv2img = self.cv2img[:, :, ::-1]
        self.states.append(self.cv2img)
        

    def save_img(self):
        """[summary]
        """
        save_img = Image.fromarray(self.cv2img)
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename is None:
           return
        save_img.save(filename)
        
    def face_detect(self):
        """[summary]
        """
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.gray = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2GRAY)
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
       
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        for (x, y, w, h) in faces:
            self.cv2img = cv2.rectangle(self.cv2img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
        faceimg = Image.fromarray(self.cv2img)
        faceimg = ImageTk.PhotoImage(faceimg)
        self.panel.configure(image = faceimg)
        self.panel.image = faceimg
        
        self.btn.pack(side = 'right')
        self.states.append(self.cv2img)
        
    def crop_face(self):
        """[summary]
        """
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)
        self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
        face_crop = []
        for f in faces:
            x, y, w, h = [ v for v in f ]
            
            # Define the region of interest in the image  
            face_crop.append(self.cv2img[y:y+h, x:x+w])

        for face in face_crop:
            cv2.imshow('Press s to save cropped image',face)
            self.cv2img = cv2.cvtColor(self.cv2img, cv2.COLOR_BGR2RGB)
            k = cv2.waitKey(0) & 0xFF
            if k == 27:         # wait for ESC key to exit
                cv2.destroyAllWindows()
            elif k == ord('s'): # wait for 's' key to save and exit
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                save_img = Image.fromarray(face)
                filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
                save_img.save(filename)
                cv2.destroyAllWindows()
        self.btn.pack_forget()

            
    def crop_img(self):
        """[summary]
        """
        self.cv2img = self.cv2img[0:300, 0:400]
        crop_image = Image.fromarray(self.cv2img)
        crop_image = ImageTk.PhotoImage(crop_image)
        self.panel.configure(image = crop_image)
        self.panel.image = crop_image
        self.states.append(self.cv2img)

        
    def exitProgram(self):
        """[summary]
        """
        os._exit(0)
        
        
if __name__ == '__main__':

    root=Tk()
    ph=ImageProcessor(root)
    root.geometry("1920x1060")
    root.mainloop()
