#!/usr/bin/env python

import cv2
import numpy as np
import processData

np.random.seed()
image_names, steering_angles = processData.get_csv_data("data/driving_log.csv")

id = np.random.randint(0,len(image_names))
img_id = np.random.randint(0,3)
image = cv2.imread("data" + "/" + image_names[id][img_id])
image = processData.process_image(image)
cv2.imshow("Image" , image)
cv2.waitKey(0)
