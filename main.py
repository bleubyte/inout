#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import datetime as dt
import time
import schedule
import boto3
import os
from random import randint
import random

# pip install pip install selenium schedule boto3


def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.dirname(__file__)
	return os.path.join(base_path, relative_path)


def fBrowser():
	chrome_options =  webdriver.ChromeOptions()
	chrome_options.add_argument("--window-size=800x600")
	#chrome_options.add_argument("user-data-dir=selenium")
	chrome_options.add_argument('--no-sandbox')
	#chrome_options.add_argument('--headless')
	chrome_options.add_argument('--ignore-certificate-errors')
	driver = webdriver.Chrome(options=chrome_options, executable_path=resource_path('./driver/chromedriver.exe'))
	driver.get('https://www.simpleinout.com/en/users/sign_in')
	time.sleep(5)
	# optional look at page title do actions
	driver.find_element_by_name('user[email]').send_keys('Email@address.com') 
	driver.find_element_by_name('user[password]').send_keys('YourPass') 
	driver.find_element_by_xpath('//*[@id="new_user"]/div[3]/div/input').send_keys(Keys.RETURN) # submit button
	driver.find_element_by_xpath('//*[@id="slow"]/form/p[2]/input[3]').send_keys(Keys.RETURN) #.click() # Update button
	time.sleep(15)
	driver.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[5]/a').click() # Log off page
	time.sleep(15)
	driver.close()
	# Create a Log file
	GetDateNow = datetime.datetime.now()
	StringDate = str(GetDateNow.strftime("%d/%m/%Y %H:%M:%S"))
	with open("log.txt", mode='a') as file:
		file.write('Task completed at {} \n'.format(StringDate))

	# Send SMS notification
	client = boto3.client('sns',aws_access_key_id='PutYourKEYhereForSmSNotification',aws_secret_access_key='PutYourKEYhereForSmS',region_name='ap-southeast-1')
	sms_txt = 'I have completed the task at {}'.format(StringDate)
	print(sms_txt)
	client.publish(PhoneNumber='+971xxxxxxxxx',Message=sms_txt)



class RandomDates:
	def __init__(self):
		self.numberList = [5]
		self.StartWork = random.choice(self.numberList)
		self.numberList2 = [0]
		self.EndWork = random.choice(self.numberList2)
		self.end_min = randint(0, 8)
		self.WorkOn = str('07:{}{}'.format(self.StartWork,self.end_min)) 
		self.WorkOff = str('16:{}{}'.format(self.EndWork,self.end_min)) 

def GetNumbers():
	return RandomDates() 
      
# Driver code to test above method 



global TimeTicker
TimeTicker = GetNumbers()
print('Logging in at {}'.format(TimeTicker.WorkOn)) 
print('Logging off at {}'.format(TimeTicker.WorkOff))
time.sleep(3)

def Randomtime():
	TimeTicker = GetNumbers()
	print('Logging in at {}'.format(TimeTicker.WorkOn)) 
	print('Logging off at {}'.format(TimeTicker.WorkOff))
	time.sleep(10)
	return TimeTicker



schedule.every().day.at(TimeTicker.WorkOn).do(fBrowser)
schedule.every().day.at(TimeTicker.WorkOff).do(fBrowser)



while True:
	now = dt.now()
	print("[i] Running Current System Time =", now.strftime("%H:%M:%S"),  sep=' ', end='\r', flush=True)
	schedule.run_pending()

	localtime = time.localtime(time.time())
	x = localtime[3:5]
	if x == (23, 59):
		TimeTicker = GetNumbers()
		print('[i] Updated Daily Random time')
		time.sleep(60)

	time.sleep(1)
