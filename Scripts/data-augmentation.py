'''
/**
* 2/2021
* Pontifícia Universidade Católica de Minas Gerais
* Advisor - Prof. Alexei Machado
* Designed by:
* @author Igor Machado Seixas - 561897
* @version 0.10a
*/
'''

'''
/**
* Libraries:
* PIL
*/
'''

import os
from PIL import Image
from PIL import ImageOps

# Function to translate images.
# Param img_folder - contains the image folder path.
def translate_augmentation(img_folder):
    global backgroun_w
    global backgroun_h

    # Iteract in the files directory.
    for dir in os.listdir(img_folder):
        for file in os.listdir(os.path.join(img_folder, dir)):
            image_path = os.path.join(img_folder, dir,  file)
            image = Image.open(image_path)

            # Check if directory exists.
            Exist = os.path.exists(f"{img_folder}{dir}-translate_augmentation")
            if not Exist:
                os.mkdir(f"{img_folder}{dir}-translate_augmentation")

            # Create a image with green background.
            background_img = Image.new(mode="RGB", size=(backgroun_w,backgroun_h), color=(0,255,0))

            # Get the max rectangle from image.
            max_rect = image.getbbox()

            # Create and offset get the relative point so the final_img_crop will be at center position.
            offset = ((background_img.size[0] - image.size[0])//2, (background_img.size[1] - image.size[1])//2)

            # Pasting the cropped image over the original image with green and mask background.
            background_img.paste(image, offset, image)
            background_img.save(f"{img_folder}{dir}-translate_augmentation/t_{file}", quality=100)

            

# Funciton to rotate images.
# Param img_folder - contains the image folder path.
# Param rotation angle - angle which you want to be rotated.
def rotate_augmentation(img_folder, rotation_angle):
    # Iteract in the files directory.
    for dir in os.listdir(img_folder):
        if not "-rotate_augmentation" in dir and not "-mirroring_augmentation" in dir:
            for file in os.listdir(os.path.join(img_folder, dir)):
                image_path = os.path.join(img_folder, dir,  file)
                image = Image.open(image_path)

                # Check if directory exists.
                Exist = os.path.exists(f"{dir}") #{img_folder}{dir}-rotate_augmentation
                if not Exist:
                    os.mkdir(f"{dir}") #{img_folder}{dir}-rotate_augmentation

                # Rotate according to rotation_angle and save the image in a new directory.
                angle = int(360/rotation_angle)
                for i in range(1,angle):
                    rotated_image = image.rotate(i*rotation_angle)
                    rotated_image.save(f"{dir}/r_{i}_{file}", quality=100) #{img_folder}{dir}-rotate_augmentation

# Function to mirror images.
# Param img_folder - contains the image folder path.
def mirroring_augmentation(img_folder):
    # Iteract in the files directory.
    for dir in os.listdir(img_folder):
        if not "-mirroring_augmentation" in dir:
            for file in os.listdir(os.path.join(img_folder, dir)):
                image_path = os.path.join(img_folder, dir,  file)
                image = Image.open(image_path)

                # Check if directory exists.
                Exist = os.path.exists(f"{dir}") #{img_folder}{dir}-mirroring_augmentation
                if not Exist:
                    os.mkdir(f"{dir}") #{img_folder}{dir}-mirroring_augmentation
                
                # Mirror and save image in a new directory.
                mirror_image = ImageOps.mirror(image)
                mirror_image.save(f"{dir}/m_{file}", quality=100) #{img_folder}{dir}-mirroring_augmentation

# Function to augmentate data. Execute roation and mirroring in the images.
# Param img_folder - contains the image folder path.
# Param rotation angle - angle which you want to be rotated.
def data_augmentation(img_folder, rotation_angle):
    #translate_augmentation(img_folder)
    #rotate_augmentation(img_folder, rotation_angle)
    mirroring_augmentation(img_folder)

img_folder = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\thyroid-crop-small-background-square-160-train"
backgroun_w = 360
backgroun_h = 360

data_augmentation(img_folder, 45)
#increased_dataset = torch.utils.data.ConcatDataset([transformed_dataset,original])