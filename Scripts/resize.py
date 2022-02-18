

from PIL import Image
import os
import PIL
import glob

dir = "quarentena/4"
images = [file for file in os.listdir(dir) if file.endswith(('jpeg', 'png', 'jpg'))]
for image in images:
    img = Image.open(f"{dir}/{image}")
    resized_image = img.resize((224,224))
    resized_image.save(f"{dir}-resize/"+image, quality=96)

