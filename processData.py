#!/usr/bin/env python
##Author: rsalem
##Purpose: Fetch data and Pre-Process images
from __future__ import print_function
#imports
import os
import cv2
import csv
import random
import numpy as np


# Resize image
def resize_image(image):

    return cv2.resize(image, (200,66), interpolation = cv2.INTER_AREA)

# Normalize the image so that input data values range between -1 and 1
def normalize_image(image):

    return image/127.5-1

# Cropping the image to remove the un-necessary top (sky) and bottom pixels (bonet)
def crop_image(image):

    return image[140:-120,:]

def random_brightness(image):
	# randomly select the gamma values
    gamma = random.uniform(0.5,2.2)
    # Using the formula O=I^(1/G) O=output image, I = input image, G = Gamma
    inverseGamma = 1.0 / gamma
    # build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
    table = np.array([((i / 255.0) ** inverseGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
    return cv2.LUT(image, table)

# Combine all the processing for the images: crop->resize->random_brightness
def process_image(image):

     image = crop_image(image)
     image = resize_image(image)
     image = random_brightness(image)

     return  image
