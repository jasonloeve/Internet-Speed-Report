#!/usr/bin/python

import os
import sys
import MySQLdb
import datetime
import time

# Run speedtest-cli

print 'Running speed test....'
speed = os.popen("speedtest-cli --simple").read()
print 'Speed test completed'

# Split the 3 line result (ping,down and up)

lines = speed.split('\n')
print speed
ts = time.time()
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
print now,p, d, u

# Open database connection

db = MySQLdb.connect("localhost","DBUSERNAME","DBPASSWORD","DBNAME")

# prepare a cursor object using cursor() method

cursor = db.cursor()

# SQL query to INSERT a record into the table

cursor.execute('''INSERT into speed_test (id, isp_test_time, isp_name, isp_ping, isp_result_download, isp_result_upload)
              values (null, %s, 'Wireless Nation', %s, %s, %s)''',
              (now,p,d,u))

# Commit your changes in the database

db.commit()

# Disconnect from server

db.close()
