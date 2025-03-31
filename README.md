# CM-3070-Final-Project
# Surveillance System with Intrusion Detection

This project is a home surveillance system built using Flask, MySQL, OpenCV, YOLO object detection, and email notifications. The system captures video feeds from cameras, performs real-time intrusion detection, and sends email alerts when an intrusion is detected. It provides a full-stack solution for monitoring and alerting in home security environments.

## Features

- **User Authentication**: Secure login with Flask-Login to manage user access.
- **Real-Time Object Detection**: Utilizes the YOLOv8 model to detect human intruders and track movements.
- **Email Notifications**: Sends email alerts for intrusion detection (using Gmail's SMTP service).
- **Camera Video Feed Management**: Integrates video streams from multiple cameras, managed via a MySQL database.
- **Local Video Storage**: Saves intrusion videos for later retrieval.
- **Web Application Interface**: Flask-based web interface for camera monitoring, settings management, and video playback.

## Installation

### Prerequisites

- Python 3.x
- MySQL database (local or remote)
- Gmail account for email notifications

### Required Packages

Please install the packages listed in the requirement.txt file. How to install the packages is stated in the text file more clearly for both Windows and Mac users.

### Database

This application requires MYSQL database to run. There is both the query file and SQL database dump file inside the database folder to be used in the application. After downloading the sql files, please also configure the database access in the main application python file - flask-app.py

## Contents

### Templates Folder

Where the html pages for the web application are stored.

### Static Folder

This folder is used to called video files. There are two main folders inside, 
- intrusion videos folder: Intrusion videos are stored here and also callable from the database.
- test videos folder: Contains a tester video for testing the YOLOv8 model.

### Use Case Testings

#### 1. Motion Detection and Intrusion Tagging
Tests that prove YOLOv8 model detects human objects in real-time video feeds. The system tracks the detected objects and identifies them based on predefined zones.

#### 2. Camera Index Identification
Tests for the system to ensures that the correct cameras are selected, even if the camera order changes due to reconnections.

# How to Run
The main application code base is the flask-app.py. After setting up the Prerequisites and Requirements including the database, can run it by writing **python flask-app.py** in the terminal.
The web application will be Running on **http://127.0.0.1:5000**

##Acknowledgments

- YOLOv8 for real-time object detection.
- Flask for building the web application.
- OpenCV for video processing.
- MySQL for database management.

