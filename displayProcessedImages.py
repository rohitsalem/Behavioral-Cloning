#!/usr/bin/env python

import cv2
import numpy as np
import processData

np.random.seed()
image_names, steering_angles = processData.get_csv_data("data/driving_log.csv")

id = np.random.randint(0,len(image_names))
img_id = np.random.randint(0,3)
image = cv2.imread("data" + "/" + image_names[id][img_id])
image_brightness1 = processData.random_brightness(image)
image_crop = processData.crop_image(image_brightness1)
image_resize = processData.resize_image(image_crop)
image_brightness2 = processData.random_brightness(image)
image_brightness3 = processData.random_brightness(image)
cv2.imwrite("random_brightness1.jpg" , image_brightness1 )
cv2.imwrite("random_brightness2.jpg" , image_brightness2 )
cv2.imwrite("random_brightness3.jpg" , image_brightness3 )
cv2.imwrite("crop_image.jpg" , image_crop)
cv2.imwrite("processed_image.jpg" , image_resize)
cv2.imshow("image_brightness1" , image_brightness1)
cv2.imshow("image_brightness2" , image_brightness2)
cv2.imshow("image_brightness3" , image_brightness3)
cv2.imshow("image_crop" , image_crop)
cv2.imshow("final_image", image_resize)
cv2.waitKey(0)
