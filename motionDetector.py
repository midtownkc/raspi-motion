#!/usr/bin/python
# This program uses a motion detector, takes a pic and
# sends an SMS if motion is detected.
# Tested on Raspberry Pi 3, No-IR Filter PiCamera 2.0
# Shout out to Mike Haldas for the sms & imgur code
# http://bit.ly/2ljRJqc
# Account credentials masked ~ ~ 
# maxwell.frederickson@gmail.com
#
import pyimgur
import picamera
from gpiozero import MotionSensor
from twilio.rest import TwilioRestClient

DELAY = 0 #If you want a delay between detection and photo

#Twilio Account Credentials
ACCOUNT_SID ="AC230bd"
AUTH_TOKEN = "facb12"

#phone to text, also phone from twilio
TO_PHONE = "+15555555555"
FROM_PHONE ="+15555555555"

#Message to text:
TXT_MSG = "Motion Detected."

#Directory to store image
IMAGE_DIR = "/home/pi/Documents/motion/"

#imgur client setup
CLIENT_ID = "f5db"

#image file will be overwritten
IMG = "snap.jpg" 
IMG_WIDTH = 2592
IMG_HEIGHT = 1944

#initialize Twilio
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

#initialize imgur
im = pyimgur.Imgur(CLIENT_ID)

#define motion sensor
pir = MotionSensor(4)

while True:
	if pir.motion_detected:
		print("Motion Detected!\n")
		pir.wait_for_motion()
		#time.sleep(DELAY)  #if wanted to set delay between detection and pic
		with picamera.PiCamera() as camera:
			camera.resolution = (IMG_WIDTH, IMG_HEIGHT)
			camera.capture(IMAGE_DIR + IMG)
				
		uploaded_image = im.upload_image(IMAGE_DIR + IMG, title=TXT_MSG)
		client.messages.create(
				to=TO_PHONE,
				from_=FROM_PHONE,
				body=TXT_MSG,
				media_url=uploaded_image.link,
		)
			
			
