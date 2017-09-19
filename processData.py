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

BatchSize = 64

# Resize image
def resize_image(image):
    return cv2.resize(image, (200,66), interpolation = cv2.INTER_AREA)

# Normalize the image so that input data values range between -1 and 1
def normalize_image(image):
    return image/127.5-1

# Cropping the image to remove the un-necessary top (sky) and bottom pixels (bonet)
def crop_image(image):
    return image[40:-20,:]

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

# Read the CSV file for image location and steering angle
def get_csv_data(file):
    image_names, steering_angles = [],[]
    steering_offset = 0.27 # Offset for left and right cameras
    with open(file,'r') as f:
        reader = csv.reader(f)
        next(reader,None)
        for center_img, left_img, right_img, steering, _ , _ , _ in reader:
            angle = float(steering)
            image_names.append ([center_img.strip() , left_img.strip(), right_img.strip()])
            steering_angles.append([angle , angle + steering_offset, angle  - steering_offset])
    return image_names, steering_angles

# Fetch image filenames and steering_angles randomly while limiting the number of straight path(angle=0) data
def fetch_images(X_train, y_train, batch_size):
    thresh = 0.1
    count = 0 # counter for producing #batch_size number of images
    zero_count = 0
    images_and_angles = [] # to store image file names and angles
    while (count < batch_size):
        index = np.random.randint(0,len(X_train))
        angle = y_train[index]
        image = X_train[index]
        # print (angle)
        if(-thresh<angle[0]<thresh):
            if(zero_count<15):
                images_and_angles.append((image,angle))
                zero_count = zero_count + 1
                count = count + 1
        else:
            images_and_angles.append((image,angle))
            count = count + 1

    return images_and_angles

# To generate_batch of images and angles
def generate_batch(X_train, y_train, batch_size=BatchSize):
    while True:
        X_batch = []
        y_batch = []
        images_and_angles = fetch_images(X_train, y_train, batch_size)
        # To read images from the list feteched using the fetch_images function
        # print (images_and_angles)
        for image_file , angle in images_and_angles:
            # To ranomly select left/center/right image
            ind  = np.random.randint(0,3)
            raw_image = cv2.imread("data" + "/" + image_file[ind])

            raw_angle = float(angle[ind])
            # Process the image before yielding the dataset
            image = process_image(raw_image)
            # Randomly flipping the image ans steering_angle
            if random.randrange(2)==1:
                image = cv2.flip(image,1)
                raw_angle = -raw_angle
            X_batch.append(image)
            y_batch.append(raw_angle)
        assert len(X_batch) == batch_size, 'len(X_batch) == batch_size should be True'
        yield np.array(X_batch), np.array(y_batch)
