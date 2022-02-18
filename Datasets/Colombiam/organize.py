import os
from tkinter import filedialog
import xml.etree.ElementTree as ET
import shutil

# Configuration variables.

path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\thyroid-full"
indefined_path = "C:\\Users\\igormseixas\\TCC_II\\Datasets\\Colombiam\\thyroid-full\\Undefined"

def open_xml():
	global path

	if len(path) > 0:
		for filename in os.listdir(path):
			if not filename.endswith('.xml'): continue
			fullname = os.path.join(path, filename)
			
			# Open XML and get roots.
			xml = ET.parse(fullname)
			root = xml.getroot()

			tirads = root[7].text
			xml_number = root[0].text

			# Copy file to respective folder
			if tirads is not None:
				copy_path = path+"\\"+tirads+"\\"+filename
				# Copy XML		
				shutil.copyfile(fullname, copy_path)
				# Copy IMG
				copy_image(xml_number, tirads)
			else:
				# Copy XML
				shutil.copyfile(fullname, indefined_path+"\\"+filename)
				# Copy IMG
				copy_image(xml_number, "Undefined")

def copy_image(xml_number, tirads):
	for imagename in os.listdir(path):
		if not imagename.startswith(xml_number+"_"): continue
		fullimagename = os.path.join(path, imagename)
		image_copy_path = path+"\\"+tirads+"\\"+imagename
		only_image_copy_path = path+"\\"+tirads+"\\only_img\\"+imagename	
		
		shutil.copyfile(fullimagename, image_copy_path)
		shutil.copyfile(fullimagename, only_image_copy_path)

def get_name(filename, tirads, root):
	# Get the name of a specific tirads
	if tirads == "2" and root[1].text == "24":
		print(filename)

def rename_tirads():
	print("BLA")