# AI_Driven_Crop_Optimization_For_Sustainable_Farming
# Overview
AI Driven Crop Optimization for Sustainable Farming is an IoT and deep-learning based smart agriculture project designed to support farmers with crop monitoring, plant-disease identification, environmental sensing, and automated farm control.
The project combines a Raspberry Pi-based system, environmental sensors, a camera, deep-learning-based image classification, an LCD display, ThingSpeak cloud communication, and a mobile application interface.
The project abstract describes the system as a Virtual Smart Farm Advisor that uses AI-driven insights for crop recommendations, irrigation scheduling, and fertilizer optimization. It also describes a simulation-based IoT model using generated temperature, humidity, soil moisture, pH, rainfall, light-intensity, and NPK data. 
The current implementation additionally contains a Raspberry Pi camera, DHT22 sensor, soil-moisture input, pump outputs, YOLO-based plant-disease detection, ThingSpeak communication, and multilingual recommendations.  
# Main Features
- Temperature and humidity monitoring using DHT22
- Soil-moisture monitoring
- Raspberry Pi camera-based plant image capture
- YOLO-based plant disease/leaf classification
- Disease-specific recommendations
- LCD display for sensor readings and detection results
- ThingSpeak cloud communication
- Remote trigger mechanism through ThingSpeak
- Pump/output control
- Multilingual detection and recommendation output
- Digital smart-farming dashboard/application concept
- AI-assisted crop and plant-condition monitoring
# System Components
# Hardware
- Raspberry Pi
- Raspberry Pi Camera
- DHT22 Temperature and Humidity Sensor
- Soil Moisture Sensor
- 16x2 LCD
- Pump
- Motor driver module
- GPIO-controlled outputs
- Connecting wires and power supply
The uploaded circuit image shows the Raspberry Pi connected with a DHT22 sensor, motor-driver/pump section, soil-moisture sensor, and LCD display.
# Software and Technologies
- Python
- Raspberry Pi GPIO
- OpenCV
- YOLO / Ultralytics
- Picamera2
- Adafruit DHT
- ThingSpeak API
- Google Translator
- LCD control through GPIO
- Deep learning for plant/leaf classification
# System Workflow
```text
Environmental Sensors
        |
        v
Temperature / Humidity / Soil Moisture
        |
        v
     Raspberry Pi
        |
        +--------------------+
        |                    |
        v                    v
   LCD Display          Camera Capture
                             |
                             v
                         YOLO Model
                             |
                             v
                    Plant / Leaf Detection
                             |
                             v
                  Disease Classification
                             |
                             v
                    Recommendation
                             |
                +------------+------------+
                |                         |
                v                         v
           LCD Display              ThingSpeak
                                          |
                                          v
                                  Mobile / Dashboard
```
# Plant Disease Detection
The implementation uses an Ultralytics YOLO model loaded from:
```text
best.pt
```
A camera frame is captured and saved before being passed to the model for prediction. The detected class labels are then used to generate recommendations.  
The implementation includes recommendations for several plant and leaf conditions, including:
- Apple leaf conditions
- Bell pepper leaf conditions
- Corn leaf conditions
- Potato leaf conditions
- Tomato leaf conditions
- Grape leaf conditions
- Strawberry leaf
- Raspberry leaf
- Soyabean leaf
- Squash powdery mildew
The recommendation mapping is defined in the Python implementation. 
# Sensor Monitoring
The DHT22 is used to obtain temperature and humidity readings. The soil-moisture input is also read through a Raspberry Pi GPIO pin.
The values are displayed on the LCD and printed during operation. 
Example display format:
```text
T:28.0C
H:65.0% M:1
```
# LCD Output
The LCD provides local information without requiring the user to continuously access the application.
It can display:
- Temperature
- Humidity
- Soil moisture status
- Detected plant/leaf condition
- Translated detection output
The LCD is initialized and controlled directly through Raspberry Pi GPIO pins.  
# ThingSpeak Integration
ThingSpeak is used for cloud-based communication between the Raspberry Pi system and the remote interface.
The implementation:
- Reads a trigger value from ThingSpeak
- Sends detected plant/disease information
- Sends temperature
- Sends humidity
- Sends soil-moisture status
- Sends the generated recommendation
The implementation uses multiple ThingSpeak fields for this information.  
## Multilingual Support
The system supports translated detection results and recommendations.
The current Python implementation sets:
```python
LANGUAGE = "te"
```
for Telugu output, with comments indicating support for Hindi, Tamil, Malayalam, Kannada, and English. 
# How the System Works
1. The Raspberry Pi initializes the GPIO pins, LCD, DHT22 sensor, camera, and output controls.
2. Temperature, humidity, and soil-moisture values are read.
3. The camera continuously captures frames.
4. A trigger value is obtained from ThingSpeak.
5. When the prediction trigger is received, the current camera frame is saved.
6. The YOLO model analyzes the captured image.
7. The detected plant or leaf condition is identified.
8. A corresponding recommendation is selected.
9. The result and recommendation are translated when required.
10. The detection result is shown on the LCD.
11. Sensor values, detection results, and recommendations are uploaded to ThingSpeak.
12. GPIO outputs can be controlled according to the received trigger values.
# Project Structure
```text
AI_Driven_Crop_Optimization_For_Sustainable_Farming/
 main1.py
 best.pt
 rpi_agg1.apk
 README.md
 images/
     circuit.jpg
```
# Running the Python Application
The main Python implementation is provided in:
```text
main1.py
```
Install the required Python packages and Raspberry Pi libraries before running the application.
The implementation imports:
```python
from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import requests
import RPi.GPIO as GPIO
import Adafruit_DHT
from deep_translator import GoogleTranslator
```
These dependencies correspond to the camera, deep-learning model, image processing, cloud communication, GPIO, DHT22 sensor, and translation functions used by the project. 
## Mobile Application
The repository can also include the provided Android application:
```text
rpi_agg1.apk
```
The application is intended to provide a remote interface for the smart-agriculture system.
# Project Objectives
- Monitor important agricultural conditions.
- Identify plant and leaf conditions using deep learning.
- Provide actionable recommendations.
- Support remote monitoring through cloud communication.
- Automate selected farm-control functions.
- Provide information through a local LCD and remote interface.
- Support multilingual interaction for farmers.
The project abstract specifically identifies crop recommendation, irrigation forecasting, fertilizer optimization, visualization, and a Virtual Smart Farm Advisor as the broader project objectives. 
## Future Scope
The system can be extended with:
- More crop and disease classes
- Improved crop recommendation models
- Weather-based irrigation prediction
- Automated fertilizer recommendations
- Additional agricultural sensors
- Real-time farm dashboards
- More regional languages
- Automated irrigation and spraying
- Historical data analysis
- Improved mobile application features
# Note
The project abstract describes a simulation-based IoT model using synthetic agricultural data, while the supplied implementation demonstrates a Raspberry Pi-based physical prototype with DHT22, soil-moisture sensing, camera input, and GPIO-controlled outputs. These represent the documented project concept and the supplied implementation respectively.


