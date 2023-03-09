import cv2
import numpy as np
import matplotlib.pyplot as plt


#img = cv2.imread('284_1_crop_1.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('284_1.jpg')

h, w = img.shape[:2]

# convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# add 1 pixel white border all around
pad = cv2.copyMakeBorder(gray, 35,35,35,35, cv2.BORDER_CONSTANT, value=255)
h, w = pad.shape

# create zeros mask 2 pixels larger in each dimension
mask = np.zeros([h + 2, w + 2], np.uint8)

# floodfill outer white border with black
img_floodfill = cv2.floodFill(pad, mask, (0,0), 0, (5), (0), flags=8)[1]

# remove border
img_floodfill = img_floodfill[1:h-1, 1:w-1]

#mask = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)[1][:,:,0]
mask = cv2.threshold(img_floodfill, 0, 210, cv2.THRESH_BINARY_INV)[1][:,:]
#dst = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)

#cv2.imshow('visualize', img)
#cv2.imwrite('visualize',mask)
#cv2.imshow('visualize', dst)
#cv2.imshow('visualize', mask)
#cv2.waitKey()

plt.imshow(pad)
plt.show()