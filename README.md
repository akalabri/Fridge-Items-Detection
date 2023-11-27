# Fridge-Items-Detection
Using computer vision, the program keeps track of fridge inventory and updates the database accordingly
<iframe src="[https://drive.google.com/file/d/VIDEO_ID/preview](https://drive.google.com/file/d/1FVu9idLM0kklUQ1D7Fggxcd88dfghTv3/view?usp=drive_link)" width="640" height="480"></iframe>

# Fridge Inventory Management System

Welcome to the Fridge Inventory Management System project! This project is designed to help you keep track of the items in your fridge, detect who interacts with it, and manage the inventory effectively. Below, I will provide an overview of the project, the skills and tools used, and the steps taken to achieve the desired outcome.
![detections](https://raw.githubusercontent.com/akalabri/Fridge-Items-Detection/main/Media/detections.png)
![dashboard](https://raw.githubusercontent.com/akalabri/Fridge-Items-Detection/695306cf8e92b93aa161c6a3cfc4bf387d1fdd23/Media/dashapp.png)

## Overview

Managing the inventory of a fridge can be a challenging task, especially when multiple people have access to it. This project tackles this challenge by using computer vision and deep learning techniques to:

- Detect individuals accessing the fridge.
- Identify and track various items such as milk, biscuits, chocolate, etc.
- Update the inventory based on detected interactions.
- Visualize the inventory trends over time using a web-based dashboard.

## Skills and Tools Utilized

### Computer Vision and Object Detection
- Utilized YOLO (You Only Look Once) for real-time object detection.
- Processed video streams to identify people and items in the fridge.

### Python Programming
- Leveraged the power of Python for scripting and automation.

### Data Management
- Used CSV files to store and manage inventory data.

### Web Development
- Developed a web-based dashboard using the Dash framework to visualize inventory trends.

### Machine Learning
- Trained a YOLOv8-based model using annotated data.

### Roboflow and Data Annotation
- Employed Roboflow for annotating images extracted from videos.

### Google Colab
- Utilized Google Colab for model training, which provides access to GPUs for faster training.

## Project Execution Steps

### Data Collection
- Recorded videos of individuals interacting with the fridge.
- Extracted frames from these videos for annotation.

### Data Annotation
- Used Roboflow to annotate the extracted frames, marking objects of interest such as milk, biscuits, chocolate, and individuals' faces.
![annotate](https://raw.githubusercontent.com/akalabri/Fridge-Items-Detection/main/Media/annotating%20chocolate%20.png)
![annotate1](https://raw.githubusercontent.com/akalabri/Fridge-Items-Detection/main/Media/roboflow_annotating.png)
### Model Training
- Leveraged Google Colab to train a YOLOv8-based model using the annotated data.
- Fine-tuned the model to accurately detect items and people within the fridge.

### Real-time Object Detection
- Integrated the trained model into the project to perform real-time object detection on video streams.

### Inventory Management
- Maintained inventory records for items like milk, biscuits, chocolate, etc.
- Updated inventory counts based on detected interactions.

### Web-Based Dashboard
- Developed a user-friendly web dashboard using the Dash framework.
- Displayed the current inventory status.
- Showed a history of inventory updates.

### Inventory Trend Analysis
- Generated inventory trend plots to visualize item quantities over time.

## Getting Started

To use this Fridge Inventory Management System:

1. Clone this repository to your local machine.
2. Make sure you have the required Python libraries installed. You can use `requirements.txt` for this purpose.
3. Run the main Python script to start the real-time object detection and web dashboard.

```bash
python main.py
