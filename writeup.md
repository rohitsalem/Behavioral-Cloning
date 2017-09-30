#**Behavioral Cloning** 

[//]: # (Image References)

[image1]: ./images/architecture.png "Model Architecture"
[image2]: ./images/crop_image.jpg "Cropped Image"
[image3]: ./images/random_brightness1.jpg "Random Brightness 1"
[image4]: ./images/random_brightness2.jpg "Random Brightness 2"
[image5]: ./images/random_brightness3.jpg "Random Brightness 3"
[image6]: ./images/processed_image.jpg "Final Processed image"
[image7]: ./images/model_summary.png "Model Summary"

1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* processData.py which contains the functions to pre processdata and output image batches for training.
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* displayProcessedImages.py which displays a random image from the dataset after the pre-processing 
* model.h5 containing a trained convolution neural network 
* writeup_report.md summarizing the results


2. Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

3. Two main files are needed for training, `model.py` and `processData.py`. The `processData`.py preprocesses the data before being fed into the network for training. It also contains functions to fetch and yield batches of data that can be fed into the keras `fit.generator` function for training. The `model.py` file contains the code for training and saving the convolution neural network. 

**Model Architecture and Training Strategy**

1. I used the Nvidia's end-to-end learning for self-driving cars as the model architecture. The model takes in images as input and predicts the steering angle as output. 
The Model Architecture can be depicted in this image, taken directly from the paper:

![alt text][image1]

The Model summary from the keras function is here with little modifications to the Nvidia's architecture:

![alt text][image7]

2. Attempts to reduce overfitting in the model:
The model contains dropout layers in order to reduce overfitting and can be seen in the above picture which depicts the model summary. Having Dropouts forces not only every neuron to learn some features but also reduces overfitting!  
I also used regulaizers to penalize the weights if they are getting too biased to the dataset.

3. Model parameter tuning
The model used the Adam optimizer with initial learning rate of 0.0001. I also tuned the regularizer values if the model started overfitting. 

4. Appropriate training data
I used the dataset provided by Udacity and also added some of my own data where it was necessary like near the sharp turns.

**Approach**

Solution Design Approach:

* I used a Nvidia end-to-end model for self-driving cars as the model architecture as I already mentioned, the data was split into train and validation dataset before the training. 

* The tain data and the validation data were loaded as required by the `fit.generator()` function in keras and were generated in batches using the `dataProcess.py` file which has functions to generate them. The data was shuffled before being fed into the `fit.generator()`. 

* The data was definitely biased if seen intutively or if plotted because most of the time the car is driving straight !! implying the steering to be '0' for most of the time. To handle this baised dataset, I would load the dataset in such a way that there are not more than 50% of the data samples that are zeros, hence removing the biasing. This helped me to handle the turns 

* To reduce the overfitting, I used dropout layers and regularlizers in the layers.

* Then the model failed in some of those really sharp turns. So I collected the data at the sharp turns and added it to the main dataset, then trained the model again. Because of the increased probabiltiy of these turns being sampled, it worked after the new training process.

* Before starting the training process, I pre-processed the images to crop, resize and adjust the brightness randomly. I cropped out the unnessary part of the image which the car sees: like the bonet, top sky. Then resized the image (220,66) to fit in as the input to the network and also changed the brightness randomly to handle different lightning conditions.

Here is a sample image obtained from the dataset which has undergone the pre-processing:

Random brightness:

![alt text][image3]

![alt text][image4]

![alt text][image5]

Cropped Image:

![alt text][image2]

Resized Image/Final processed image:

![alt text][image6]

* To make use of the left and right images as well, I sampled the right and left images as well randomly along with the center images. I added an offset of `0.275` to the left image and subtracted `0.275` for the right image form the steering angle to imitiate it as a center image itself. This really made use of the limited dataset, not requiring a lot of data.

* Using the left and right images essentially made to correct the car from going off road. As it simulated what we would do when we are going to the left ramp (turn right) and vise versa, this is handled by using the steering offset! 

* The network was able to handle sharp turns also smoothly, there was a little jitter while going straight this might be because of using the the left and right images and not the right offset, it can be correct by using appropriate offset which could be obtained by trail and error.

* The video of the run can be found [here](https://youtu.be/BKlFEks0HgM)
