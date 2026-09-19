# =========================================================
# LIVE CAMERA PREVIEW + YOLO TRIGGER CAPTURE
# =========================================================

from picamera2 import Picamera2
from ultralytics import YOLO
import cv2
import requests
import time
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
from deep_translator import GoogleTranslator
# ================= DHT22 =================
sensor = Adafruit_DHT.DHT22   # ✅ DHT22
gpio = 4
ms=3
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ================= LCD PINS =================
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11

p1 = 17
p2 = 27

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.0005
E_DELAY = 0.0005
GPIO.setup(ms, GPIO.IN)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

GPIO.setup(p1, GPIO.OUT)
GPIO.setup(p2, GPIO.OUT)
GPIO.output(p1,0)
GPIO.output(p2,0)

LANGUAGE = "te"   # Telugu
# hi = Hindi
# ta = Tamil
# ml = Malayalam
# kn = Kannada
# en = English
RECOMMENDATIONS = {
    "Apple Scab Leaf": "Apply fungicide and remove infected leaves",
    "Apple leaf": "Plant is healthy, maintain proper irrigation",
    "Apple rust leaf": "Use sulfur fungicide and prune affected areas",

    "Bell_pepper leaf spot": "Apply copper fungicide and avoid overhead watering",
    "Bell_pepper leaf": "Healthy plant, continue balanced fertilization",

    "Blueberry leaf": "Healthy leaf, maintain soil acidity",

    "Cherry leaf": "Healthy leaf, monitor for fungal infection",

    "Corn Gray leaf spot": "Apply fungicide and rotate crops",
    "Corn leaf blight": "Use resistant varieties and fungicide",
    "Corn rust leaf": "Apply fungicide and ensure airflow",

    "Peach leaf": "Healthy plant, regular pruning recommended",

    "Potato leaf early blight": "Use fungicide and remove infected leaves",
    "Potato leaf late blight": "Apply systemic fungicide immediately",
    "Potato leaf": "Healthy leaf, monitor moisture levels",

    "Raspberry leaf": "Healthy plant, ensure good drainage",

    "Soyabean leaf": "Healthy leaf, apply nitrogen if needed",

    "Squash Powdery mildew leaf": "Apply sulfur spray and increase ventilation",

    "Strawberry leaf": "Healthy leaf, maintain spacing",

    "Tomato Early blight leaf": "Apply fungicide and remove affected leaves",
    "Tomato Septoria leaf spot": "Use copper fungicide and avoid wet foliage",
    "Tomato leaf bacterial spot": "Remove infected leaves and apply bactericide",
    "Tomato leaf late blight": "Immediate fungicide treatment required",
    "Tomato leaf mosaic virus": "Remove infected plant to prevent spread",
    "Tomato leaf yellow virus": "Control whiteflies and remove infected plants",
    "Tomato leaf": "Healthy leaf, continue regular care",
    "Tomato mold leaf": "Improve airflow and apply fungicide",
    "Tomato two spotted spider mites leaf": "Apply miticide or neem oil",

    "grape leaf black rot": "Apply fungicide and remove infected leaves",
    "grape leaf": "Healthy leaf, ensure proper sunlight"
}
# ================= LCD FUNCTIONS =================
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)

    GPIO.output(LCD_D4, bits & 0x10 == 0x10)
    GPIO.output(LCD_D5, bits & 0x20 == 0x20)
    GPIO.output(LCD_D6, bits & 0x40 == 0x40)
    GPIO.output(LCD_D7, bits & 0x80 == 0x80)
    lcd_toggle_enable()

    GPIO.output(LCD_D4, bits & 0x01 == 0x01)
    GPIO.output(LCD_D5, bits & 0x02 == 0x02)
    GPIO.output(LCD_D6, bits & 0x04 == 0x04)
    GPIO.output(LCD_D7, bits & 0x08 == 0x08)
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

# ================= MAIN =================
lcd_init()
lcd_string("   WELCOME", LCD_LINE_1)
time.sleep(2)

print("Reading DHT22 Sensor")

# ================= THINGSPEAK =================
READ_API_KEY = "718RJDOSQ44HN9JU"
WRITE_API_KEY = "Q4YU5KDVRKLU0G0Z"
CHANNEL_ID = "3246114"

TRIGGER_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/1/last.json?api_key={READ_API_KEY}"
UPDATE_URL = "https://api.thingspeak.com/update"

# ================= YOLO =================
model = YOLO("best.pt")

# ================= CAMERA =================
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()

print("📹 Live stream started (Press Q to quit)")

humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
mval=1-GPIO.input(ms)
if humidity is not None and temperature is not None:
    lcd_string(f"T:{temperature:0.1f}C", LCD_LINE_1)
    lcd_string(f"H:{humidity:0.1f}% "+ " M:"+str(mval), LCD_LINE_2)

    print(f"Temp={temperature:0.1f}C  Humidity={humidity:0.1f}%")
else:
    lcd_string(" Sensor Error ", LCD_LINE_1)
    lcd_string(" Check Wiring", LCD_LINE_2)
    print("Failed to read DHT22")


# ================= LOOP =================
while True:
    frame = camera.capture_array()
    cv2.imshow("Raspberry Pi Camera Stream", frame)

    trigger = 0
    try:
        r = requests.get(TRIGGER_URL, timeout=0.5)
        trigger = int(float(r.json()["field1"]))
    except:
        pass

    if trigger == 1:
        GPIO.output(p1,1)
        GPIO.output(p2,0)
    if trigger == 2:
        GPIO.output(p1,0)
        GPIO.output(p2,0)

    if trigger == 3:
        print("📸 Trigger received → Predicting")

        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        mval=1-GPIO.input(ms)
        if humidity is not None and temperature is not None:
            lcd_string('T:'+str(int(temperature))+ ' H:'+str(int(humidity))+" M:"+str(mval), LCD_LINE_1)
            

            print(f"Temp={temperature:0.1f}C  Humidity={humidity:0.1f}%")
        else:
            lcd_string(" Sensor Error ", LCD_LINE_1)
            lcd_string(" Check Wiring", LCD_LINE_2)
            print("Failed to read DHT22")


        cv2.imwrite("frame.jpg", frame)

        results = model.predict("frame.jpg", conf=0.4)
        labels = []

        for r in results:
            for c in r.boxes.cls:
                labels.append(model.names[int(c)])


        if not labels:
            result_text = "No Object"
            recommendation = "No action required"
        else:
            result_text = list(set(labels))[0]  # take first detected label
            recommendation = RECOMMENDATIONS.get(
                result_text, 
                "Monitor plant condition regularly"
            )

        try:
            translated_result = GoogleTranslator(source='auto', target=LANGUAGE).translate(result_text)
            translated_recommendation = GoogleTranslator(source='auto', target=LANGUAGE).translate(recommendation)
        except:
            translated_result = result_text
            translated_recommendation = recommendation


        lcd_string("D:"+translated_result[:16], LCD_LINE_2)

        requests.post(UPDATE_URL, data={
            "api_key": WRITE_API_KEY,
            "field1": translated_result,
            "field2": temperature,
            "field3": humidity,
            "field4": mval,
            "field5": translated_recommendation
        })

            


        print("✅ Sent:", result_text)
        time.sleep(16)

        requests.post(UPDATE_URL, data={
            "api_key": 'VBOCMH8CAMJQB7YW',
            "field1": 4
           
        })        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
camera.stop()
