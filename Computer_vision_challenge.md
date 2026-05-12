# Computer Vision (CV) Challenge

## Overview

To introduce fundamental learning methods, the CV challenge uses vision principles to offer
students firsthand experience in the end-to-end development of a training and deployment
pipeline for an ML model. Students will be provided three new “lunar” object datasets, of which
they will have to train an object detection model to use in the game. During the autonomous
game period, students will have to avoid or contact the three objects using their trained model.
Based on their performance in the game and the parameters used to train their model, they will
be scored accordingly. 

# Dataset Acquisition
## Overview
### Introduction

Students will train a YOLOv11 model, a popular state-of-the-art object detection model that can
be deployed efficiently using the Intel AIxBoard’s ONNX platform. The first essential step in
training an ML model is gathering a large amount of training data. For this model, the data must
be labeled, meaning each image also has an associated .txt file containing the coordinates of
every detected object’s bounding box (Figure 1). While this task is simple for one image, ML
models require hundreds of well-labeled images for adequate inference performance. Doing this
manually is infeasible, so it is best to leverage open-source datasets with prelabeled images.


### gather_data.py
This Python script allows the Orbit Odyssey game moderators to gather prelabeled datasets that
can then be easily provided to students. It sources images and labels from Open Images, an open
source dataset containing thousands of labeled images across hundreds of classes. Because the
labels are not in the YOLO format, additional functions convert them to the format required for
model input. Moderators can specify what classes they would like datasets for and the number of
images, with the following command:

python gather_data.py Laptop Rocket Tire --limit 200 --csv-dir "\path\to\oi_csv" --root "."

Further details on the script's contents are commented in the file. Note the folder oi_csv found
with the Python script in the shared folder. This folder must be present when running the script,
as it contains all the class-label CSV files the script references. Once the model finishes
executing, three folders containing the three datasets will be created

## Training the model
### gui_train_model.py

This Python script is the core component of the challenge (Figure 3). It provides a no-code
alternative that allows students to understand the core process of training an ML model. The first
section will enable students to upload the three dataset folders produced in the previous section.
Next to that is the hyperparameter tuning. This was one area of difficulty in finding the correct
hyperparameters that made sense for first-time students. The ones chosen are the most obvious
when it comes to training, focusing on intuitive questions like how much data should the model
be trained on vs tested on (train/test split), how quickly will the model learn (learning rate), how
advanced is the model (model size), and how long to train the model for (epoch count). Once
students have finished selecting their parameters, they can begin training the model. Training
time will vary depending on the parameters chosen. Once the model finishes training, its
performance metrics will be displayed in the bottom-right corner for students to evaluate and
compare. The trained model will also be stored in the directory for easy access in the next
section. The script can be executed with the following command:

python gui_train_model.py

### Model performance Problems
One immediate issue was that the Intel AIxBoard was not powerful enough to use this detection
model. Upon testing, the live camera feed was capped at around two frames per second (fps),
which would make it challenging to perform real-time in-game detections when the robot is
constantly moving. To improve model performance, the team leveraged the board’s ONNX
support, a model format with “optimization [which] allows the models to run efficiently and with
high performance on various hardware platforms, including CPUs, GPUs, and specialized
accelerators.” By converting the model to this format and applying FP16 quantization to reduce
memory bandwidth consumption, the model’s performance improved to around 20 fps, a
noticeable improvement that made it usable for real-time detection. While this is still a relatively
low throughput, the goal in the future is to use Intel AI-ready hardware, which should be better
able to handle these models than the low-budget AIxBoard.


## Deploying on XRP
### run__model.py
To transmit the model’s detection data to the XRP, a starting script must be run on the AIxBoard.
The run_model.py script runs the trained model and streams bounding box information to the
XRP board via a USB serial connection. One prevalent issue during this was the serial buffer
constantly overflowing due to the large volume of detections being streamed. To mitigate this,
several limiters were implemented, such as clearing the buffer after specific intervals and
streaming detections only when a new object was detected. The goal was to ensure reliable
streaming without any failures since students would not be responsible for debugging this script.
Students can also specify the confidence threshold for detections. This is a value between 0 and 1
that denotes the lower bound of the model’s confidence in classifying a detection as valid. Higher
values mean fewer detections are usually streamed. The detections are streamed in JSON format,
consisting of the class name, confidence, and xywh values of the bounding box. The program can
be run with the following command:

python run_model.py --model “model_path”--com COM5 --behaviors "0:contact,1:avoid,2:contact"

The numbers 0,1,2 correspond to the class label associated with each of the objects, and the
corresponding contact/avoid is the action taken for each. The class label pairs are available in the
metadata.yaml file in the model path folder.

### main.py

This MicroPython script is the starter script developed for students to integrate the bounding box
data with the XRP controls library. The easiest way to upload the script to the XRP is to use
Thonny. Connect the AIxBoard USB port to the micro USB port on the XRP and open Thonny.
The XRP should show under devices from which you can right-click and upload the main.py
script. The script contains a function get_bbox_data(), which, when called, reads the USB serial
buffer to obtain any detection data sent by run_model.py. Students can then write their own
control code to use the data to produce autonomous movements for the XRP in accordance with
the game requirements. This script will run automatically when the XRP is turned on. However,
to avoid premature movement, it waits for detection data to be transmitted from the
run_model.py script running on the AIxBoard. The file Game_Overview_and_Scoring.md contains
the game outline and scoring system for students to follow when programming their XRP