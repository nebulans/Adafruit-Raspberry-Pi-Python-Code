#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import gspread
from DHT_Wrapper import DHT

# ===========================================================================
# Google Account Details
# ===========================================================================

# Account details for google docs
email       = 'you@somewhere.com'
password    = '$hhh!'
spreadsheet = 'SpreadsheetName'

# ===========================================================================
# Example Code
# ===========================================================================


# Login with your Google account
try:
  gc = gspread.login(email, password)
except:
  print "Unable to log in.  Check your email address/password"
  sys.exit()

# Open a worksheet from your spreadsheet using the filename
try:
  worksheet = gc.open(spreadsheet).sheet1
  # Alternatively, open a spreadsheet using the spreadsheet's key
  # worksheet = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE')
except:
  print "Unable to open the spreadsheet.  Check your filename: %s" % spreadsheet
  sys.exit()

# Initialize sensor
d = DHT("2302", 4)

# Continuously append data
while(True):
  # Run the DHT program to get the humidity and temperature readings!
  r = d.read()
  
  if not r:
      time.sleep(3)
      continue


  print "Temperature: %.1f C" % r["temp"]
  print "Humidity:    %.1f %%" % r["hum"]
 
  # Append the data in the spreadsheet, including a timestamp
  try:
    values = [datetime.datetime.now(), r["temp"], r["hum"]]
    worksheet.append_row(values)
  except:
    print "Unable to append data.  Check your connection?"
    sys.exit()

  # Wait 30 seconds before continuing
  print "Wrote a row to %s" % spreadsheet
  time.sleep(30)
