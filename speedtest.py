#!/usr/bin/python

import os
import sys
import MySQLdb # pip install module
import datetime
import time
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Run speedtest-cli

print 'Running speed test....'

speed = os.popen("speedtest-cli --simple").read()

print 'Speed test completed'

# Split the 3 line result (ping,down and up)

lines = speed.split('\n')

print speed

ts  = time.time()
now = time.strftime('%d-%m-%Y %H:%M:%S')

# If speedtest could not connect set the speeds to 0

if "Cannot" in speed:
	p = 0
	d = 0
	u = 0

# Extract the values for ping, down and up values

else:
    p = lines[0][6:11]
    d = lines[1][10:16]
    u = lines[2][8:12]

print now, p, d, u

# Open database connection

db = MySQLdb.connect("localhost","DBUSER","DBPASSWORD","DBNAME")

# prepare a cursor object using cursor() method

cursor = db.cursor()

# SQL query to INSERT a record into the table
# Create a mySQL db with the below table and columns

cursor.execute('''INSERT into speed_test (id, isp_test_time, isp_name, isp_ping, isp_result_download, isp_result_upload)
              values (null, %s, 'ISP NAME', %s, %s, %s)''',
              (now,p,d,u))

# Commit your changes in the database

db.commit()

# Disconnect from server

db.close()

# Email Results to ISP
# Send email if internet speed is less than 50Mbs

intd 	 = int(float(d))
setvalue = int('50') # if lower than 50Mbps then email 

if setvalue  > intd: 

	# Setup email

	sender 	  = "youremail@example.com"
	recipient = "ispsupport@example.com"

	# Create message container - the correct MIME type is multipart/alternative.

	msg = MIMEMultipart('alternative')
	msg['From']    = sender
	msg['To'] 	   = recipient
	msg['Subject'] = "Poor internet speed notification - " + str(d) + "Mbps"

	# Create the body of the message (a plain-text and an HTML version).
	#text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
	html = """\
		<html>
			<head></head> 
			<body>
				<p>
					This email serves to notify you of slow internet speeds,<br>
					Our speed test conducted at """ + str(now) + """ logged the following results.
					<br><br>
					<strong>Ping</strong> | """ + str(p) + """ms<br>
					<strong>Download</strong> | """ + str(d) + """Mbps<br>
					<strong>Upload</strong> | """ + str(u) + """Mbps<br>
					<br><br>
					*Please note this email is automatically generated every 30 minutes when our internet is lower than 50Mbps.
				</p>
			</body>
		</html>
		"""

	# Record the MIME types of both parts - text/plain and text/html.

	#part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	#msg.attach(part1)
	msg.attach(part2)

	# Send the via gmail smtp
	# Allow less secure apps within gmail

	usrname  = "YOURGMAIL@gmail.com"
	password = "YOURGMAILPASSWORD"

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(usrname, password)
	server.sendmail(sender, recipient, msg.as_string())
	server.quit()

	print 'An email was sent'

else:

	print 'No email sent'