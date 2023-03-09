import os
import json

import numpy as np
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt

# Clean warnings for a cleaner console output.
os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"

# Configuration.
folder = ''
folders = ['2', '3', '4-4a', '5-4b', '6-4c', '7-5', '8-Undefined']
#img_path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\thyroid-full-img-test\\"+folder
img_path = ''
#img_crop_path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\thyroid-crop-small-background-square-test\\"+folder
img_crop_path = ''
xml_path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\xml"
img_folder_path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\svm\\thyroid-crop-small-background-square-160\\"

# Run function get_biggest_img() to get the max width and max height of all cut images.
# After that write here in the global vars.
backgroun_w = 360
backgroun_h = 360
center = [backgroun_w,backgroun_h]

def get_biggest_img():
    width_sizes = []
    height_sizes = []
    for dir in os.listdir(img_folder_path):
        print('Folder:', dir)
        for filename in os.listdir(os.path.join(img_folder_path, dir)):
            if not filename.endswith('.png'): continue
            image_path = os.path.join(img_folder_path, dir,  filename)
            width, height = Image.open(image_path).size
            width_sizes.append(width)
            height_sizes.append(height)

    print('Width Sizes:', width_sizes)
    print('Max width size:', max(width_sizes))
    print('Min width size:', min(width_sizes))
    print('Height Sizes:', height_sizes)
    print('Max height size:', max(height_sizes))
    print('Min height size:', min(height_sizes))

#get_biggest_img()

def open_xml():
    global xml_path

    if len(xml_path) > 0:
        for filename in os.listdir(xml_path):
            if not filename.endswith('.xml'): continue
            fullname = os.path.join(xml_path, filename)
            
            # Open XML and get roots.
            xml = ET.parse(fullname)
            root = xml.getroot()
            
            # Get image number.
            for mark in root.findall('mark'):
                print('XML Name:', filename)
                img_number = mark.find('image').text
                print('Image N:', img_number, '\n\n')

                svg_list = mark.find('svg').text
                #print('Json:', svg)
            
                xml_number = root[0].text
                get_svg(xml_number,root, img_number, svg_list)

def get_svg(xml_number, root, img_number, svg_list):
    global img_path
    global backgroun_w
    global backgroun_h
    
    # Plot SVG, crop image according to the mark and save.
    for filename in os.listdir(img_path):
        if not filename.endswith('.jpg'): continue
        if not filename.startswith(xml_number+'_'+img_number): continue
        
        # Get svg information with json.
        for index, svg in enumerate(sanitize_svg(svg_list)):
            # Ignore if arrow.
            if 'arrow' in svg: continue
            # Clear coordinates.
            coordinates = []
            x_coordinates = []
            y_coordinates = []

            # Open image
            print('Opening file:', filename)
            img = Image.open(img_path+'\\'+filename)
            h,w = img.size
            lum_img = Image.new('L',[h,w] ,0)

            # Comment "if" if you want to do for all images of the folder.
            #if not xml_number == '76': continue
            print('\nSVG Number:', index, '\n', svg, '\n')
            points = json.loads(svg)

            for p in points['points']:      
                # Get coordinates
                x_coordinates.append(p['x'])
                y_coordinates.append(p['y'])
                coordinates.append((p['x'], p['y']))


            # Draw points
            draw = ImageDraw.Draw(lum_img)
            for x1, y1 in coordinates[:-1]:
                for x2, y2 in coordinates[1:]:
                    draw.line([(x1,y1),(x2,y2)], fill=255, width=10)

            img_arr = np.array(img)
            lum_img_box = lum_img.getbbox()

            # Case wants to crop with background.
            #lum_img.paste((255),lum_img_box)

            lum_img_arr = np.array(lum_img)
            final_img = np.dstack((img_arr, lum_img_arr))

            print('\tBBox:', Image.fromarray(final_img).getbbox())
            #final_img_crop = Image.fromarray(final_img).crop(Image.fromarray(final_img).getbbox())
            img_bbox = Image.fromarray(final_img).getbbox()
            centerx,centery = (img_bbox[0] + img_bbox[2])//2, (img_bbox[1] + img_bbox[3])//2
            print('Center:', centerx,centery)
            deviation = 80
            final_img_crop = Image.fromarray(final_img).crop((centerx-deviation,centery-deviation,centerx+deviation,centery+deviation))
            
            print('\tImage size:', final_img_crop.size, '\n')

            # Create the back ground image and convert final_img_crop to RGB.
            #background_img = Image.new(mode="RGB", size=(backgroun_w,backgroun_h), color=(0,255,0))
            background_img = Image.new(mode="RGB", size=(final_img_crop.size[0],final_img_crop.size[1]), color=(0,0,0))

            # Create and offset get the relative point so the final_img_crop will be at center position.
            offset = ((background_img.size[0] - final_img_crop.size[0])//2, (background_img.size[1] - final_img_crop.size[1])//2)

            # Pasting the cropped image over the original image with green and mask background.
            #background_img.paste(final_img_crop, offset, final_img_crop)
            # Pasting the cropped image over the original image with square background.
            background_img.paste(final_img_crop, offset)
            
            # Show image.
            # With background.
            #background_img.show()
            # No background.
            #final_img_crop.show()

            # Save image.
            new_filename = os.path.splitext(filename)[0]
            # With background.
            background_img.save(img_crop_path+'\\'+new_filename+'_crop_'+str(index)+'.jpg')
            # No background.
            #final_img_crop.save(img_crop_path+'\\'+new_filename+'_crop_'+str(index)+'.png')

            print('Saving file:', new_filename+'_crop_'+str(index)+'.jpg\n')

            # Show plot image
            plt.imshow(Image.fromarray(img_arr), cmap='gray', vmin=0, vmax=1)
            plt.plot(x_coordinates, y_coordinates)
            #plt.show()

def sanitize_svg(svg):
    # Descripe what is not going to be at the json file.
    #"[", "],", "]","{\"points\":",
    wrong_str = [r"{}", "\"annotation\": , \"regionType\": \"freehand\"}"]

    # Add all in a json object.
    sanitized = svg
    for wr in wrong_str:
        sanitized = sanitized.replace(wr, "")

    sanitized = sanitized.replace("[{\"points", "{\"points")
    sanitized = sanitized.replace(" ", "")
    sanitized = sanitized.replace(",]", "")
    sanitized = sanitized.replace("}]", "}]}")
    #sanitized = "{\"points\": [" + sanitized + "]}"
    
    sanitized_svg = sanitized.split(",,")
    
    return sanitized_svg

for folder in folders:
    img_path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\thyroid-full-img\\"+folder
    img_crop_path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\svm\\thyroid-crop-small-background-square-160\\"+folder
    open_xml()