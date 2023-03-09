'''
/**
* 1/2022
* Pontifícia Universidade Católica de Minas Gerais
* Advisor - Prof. Alexei Machado
* Designed by:
* @author Caio Igor Vasconcelos Nazareth - 504978 
* @version 0.10a
*/
'''

'''
/**
* Libraries:
* Numpy - PIL - cv2 - tkinter
*/
'''

import cv2 as cv
import numpy as np
import os

from tkinter import *
from tkinter import filedialog

from PIL import Image as img
from PIL import ImageTk as imgTk

# Global control variables.
mainwindow = Tk() # Main instance of Tk application.

image = None
copyImage = None
originalWidth = None
originalHeight = None
image_label = None
region_window = None
copySelectedRegion = None

region_label = None

image_name = None
sequence = 1
cut_folder = "Datasets\\Colombiam\\thyroid-cut\\5\\"

# Convert image from opencv to imagetk format to show at Tk. 
# Return new image to show.
def convert_image(image):
    imageTk = cv.cvtColor(image, cv.COLOR_BGR2RGB) #ImageTk format is RGB and opencv is BGR
    imageTk = img.fromarray(imageTk)
    imageTk = imgTk.PhotoImage(imageTk)
    return imageTk

# Apply ImageTk format in the label to show at Tk.
def apply_image(image,label):
    label.configure(image=image)
    label.image = image

# Redefine image or region as it was before.
def reset_area(image_area): # Image_area True for image; False to reset region.
    global image
    global selectedRegion
    global selectedRegion_is_gray
    global zoom_in
    if (image_label is not None) and image_area:
        image = copyImage.copy() # Reset image.
        imageTk = convert_image(image)
        apply_image(imageTk,image_label)
        zoom_in = False # Removes zoom_in if True.

        region_window.destroy() # Close the select region window.
    elif (region_window is not None) and (region_window.winfo_exists()):
        selectedRegion = copySelectedRegion.copy() # Reset region.
        selectedRegion_is_gray = False # Removes selectedRegion_is_gray if True.
        selectedRegionTk = convert_image(selectedRegion)
        apply_image(selectedRegionTk,region_label)

# Open a path to choose image, save its original format in opencv and show result at ImageTk.
def open_image():
    global image
    global copyImage  
    global originalWidth
    global originalHeight
    global image_label
    global image_name
    global main_frame
    global canvas
    global sequence 

    path = filedialog.askopenfilename() # Gets path.
    sequence = 1
    if len(path) > 0:
        image = cv.imread(path, cv.IMREAD_COLOR) # Read as opencv.
        copyImage = image.copy() # Save original image.
        originalHeight = image.shape[0]
        originalWidth = image.shape[1]

        print("Image Size:")
        print(originalWidth, " x ", originalHeight)
        
        # Get the image name without extentions.
        image_name = os.path.split(path)[1]
        image_name = image_name[0:-4]

        imageTk = convert_image(image)
        # If there is no image yet, create a label at Tk to show it.
        if image_label is None:
            image_label = Label(main_frame, image=imageTk)
            image_label.image = imageTk
            image_label.bind("<Double-Button-1>", doubleclick_event) # Event with double left click at the image.
            #image_label.bind("<MouseWheel>", mousewheel_event) # Event with mousewheel click at the image.
            image_label.pack() # Create and show label/image at Tk.
            # Apply image on Canvas.   
            canvas.create_window(0,0, anchor=NW, window=image_label)
            set_scrollbar()  
        else:
            apply_image(imageTk,image_label) #if label already exists, just apply new image to it
            if (region_window is not None) and (region_window.winfo_exists()):
                region_window.destroy()
        mainwindow.title("TIRADS Recognizer - "+image_name)         

# Create blue square as selectedRegion with 128x128, makes a copy of it, create a new window for the region and show it.
def doubleclick_event(event):
    global selectedRegion
    global selectedRegion_is_gray
    global copySelectedRegion
    global region_window
    global region_label
    global sequence
    
    # Clears image before making a new sub-rect.
    image = copyImage.copy()
    # Reset the gray scale situation.
    selectedRegion_is_gray = False
    # Crop the sub-rect from the image
    region_size = 224 # Region size may change to 128, 64 and 32.
    # Making the region size as parameter, checks if it will be out of bounds first.
    # First is width.
    if (event.x-(region_size//2)) < 0: 
        region_initial_width = 0
        region_final_width = region_size-1
    elif (event.x+(region_size//2)) > originalWidth:
        region_initial_width = originalWidth - region_size
        region_final_width = originalWidth - 1
    else: # If it has space from both sides.
        region_initial_width = event.x-(region_size//2)
        region_final_width = (event.x+(region_size//2))
    # Same for height.
    if (event.y-(region_size//2)) < 0:
        region_initial_height = 0
        region_final_height = region_size-1
    elif (event.y+(region_size//2)) > originalHeight:
        region_initial_height = originalHeight - region_size
        region_final_height = originalHeight - 1
    else:
        region_initial_height = event.y-(region_size//2)
        region_final_height = (event.y+(region_size//2))
    # Crop region within range.
    overlay = image[region_initial_height:region_final_height, region_initial_width:region_final_width]
    # Copy information to a selected image.
    selectedRegion = overlay.copy()

    # Save the selected region.
    image_path = cut_folder+image_name+'_cut_seq_'+str(sequence)+'.jpg' 
    cv.imwrite(image_path, selectedRegion)
    sequence = sequence + 1

    # Define a blue rectangle in the same shape as previously selected.
    blue_rect = np.full(overlay.shape, (255,0,0), dtype=np.uint8) #Build rectangle and set the blue color (255,0,0)
    # Add the rectangle to the selected and previously cut area of an image. Scale the transparency.
    #cv.addWeighted(overlay, 0.5, blue_rect, 0.5, 1.0)
    transparency=0.7 #Greater the value, greater the transparency is.
    gamma=10.0 # Gamma of the selected area, more gamma more white will me added.
    select = cv.addWeighted(overlay, transparency, blue_rect, 1-transparency, gamma)
    image[region_initial_height:region_final_height, region_initial_width:region_final_width] = select
    # Convert and show at Tk.
    imageTk = convert_image(image)
    apply_image(imageTk,image_label)
    
    copySelectedRegion = selectedRegion.copy() # Save original region.
    #Show area of interest in another window.
    selectedRegionTk = convert_image(selectedRegion)
    # Get mainwindow window position.
    x = mainwindow.winfo_width() + mainwindow.winfo_x()
    y = mainwindow.winfo_y()
    # If there is no window for it yet, creates one; else, just updates it.
    if region_window is None:
        region_window = Toplevel()
        region_window.title("Região")
        region_label = Label(region_window,image=selectedRegionTk) # Creating new label for region inside new window.
        region_label.image = selectedRegionTk
        region_label.pack(side = TOP, pady = 10) # Show region.
        #250x180 is the box of the window. x+100 is the padding of the width, and y + 0 is the padding of the height.
        region_window.geometry("%dx%d+%d+%d" % (250, 180, x + 100, y + 0)) 
        region_window.mainloop() # Starts new window.
    else:
        # Makes sure if the window is still open; if not, recreate it.
        if region_window.winfo_exists():
            # Reset the transformations of the image.
            apply_image(selectedRegionTk,region_label)
        else:
            region_window = Toplevel()
            region_window.title("Region")
            region_label = Label(region_window,image=selectedRegionTk) # Creating new label for region inside new window.
            region_label.image = selectedRegionTk
            region_label.pack(side = TOP, pady = 10) # Show region.
            #250x180 is the box of the window. x+100 is the padding of the width, and y + 0 is the padding of the height.
            region_window.geometry("%dx%d+%d+%d" % (250, 180, x + 100, y + 0)) 
            region_window.mainloop() # Starts new window.

# Configure Main Menu.
def configure_menu(menu):
    #File Menu.
    file_menu = Menu(menu, tearoff=0) # Tearoff=0 makes the menu cleaner.
    menu.add_cascade(label="File",menu=file_menu) # Add menu cascade for file.
    file_menu.add_command(label ='New File', command = None)
    file_menu.add_command(label="Open...",command=open_image) # Open option inside file menu.
    file_menu.add_command(label ='Save', command = None)
    file_menu.add_separator()
    file_menu.add_command(label ='Clear', command=lambda: reset_area(image_area=True))
    file_menu.add_separator()
    file_menu.add_command(label ='Exit', command = mainwindow.destroy)

# Set Main Menu.
def set_menu():

    # Create Main Menu.
    menu = Menu(mainwindow)
    mainwindow.configure(menu=menu)
    configure_menu(menu) #Procedure to create our menu.

# Set Scroll Bar.
main_frame = Frame(mainwindow)
main_frame.pack(expand=YES, fill=BOTH)

canvas = Canvas(main_frame, relief=SUNKEN)  
canvas.config(scrollregion=(0,0,4000, 4000))


# Set Scroll Bar.
def set_scrollbar():
    global main_frame
    global canvas

    v = Scrollbar(main_frame, orient=VERTICAL)
    h = Scrollbar(main_frame, orient=HORIZONTAL) 
    
    v.pack(side=RIGHT, fill=Y)
    h.pack(side=BOTTOM, fill=X)
    canvas.pack(side=LEFT, expand=YES, fill=BOTH)  

    v.config(command=canvas.yview)
    h.config(command=canvas.xview)
    
    canvas.config(yscrollcommand=v.set)
    canvas.config(xscrollcommand=h.set)

    


mainwindow.title("TIRADS Recognizer")
#mainwindow.geometry("800x600") # Set size of the Main Window.
mainwindow.minsize(800,600)
mainwindow.geometry("+500+75") # Move the main window to 500, 75 on the screen.

set_menu()

# Runs final application.
mainwindow.mainloop()