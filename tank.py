#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import required modules
import time
import datetime
import RPi.GPIO as GPIO
import os
import ftplib
import mysql
import mysql.connector

GPIO.setwarnings(False)

# define server data
ftpserver = "ip.to.the.server"
ftpuser = "username"
ftppassword = "password"
ftppath = "/web"

sqlhost = "ip.to.the.server"
sqlport = "3307" # mostly Port 3306 is used, but my Synology is using 3307
sqluser = "username"
sqlpassword = "password"
sqldb = "Tank"

# define GPIO pins
GPIOTrigger = 18
GPIOEcho    = 24

# function to measure the distance
def MeasureDistance():
  # set trigger to high
  time.sleep(0.2)
  GPIO.output(GPIOTrigger, True)

  # set trigger after 40µs to low10Ã
  time.sleep(0.00004)
  GPIO.output(GPIOTrigger, False)

  # store initial start time
  StartTime = time.time()

  # store start time
  while GPIO.input(GPIOEcho) == 0:
    StartTime = time.time()

  # store stop time
  while GPIO.input(GPIOEcho) == 1:
    StopTime = time.time()

  # calculate distance
  TimeElapsed = StopTime - StartTime
  Distance = (TimeElapsed * 34400) / 2
  
  return Distance

print("Messe Volumen...")

# main function
def main():
  try:
#    while True:
      Distance0 = MeasureDistance()
      Distance01 = MeasureDistance()
      Distance02 = MeasureDistance()
      Distance03 = MeasureDistance()
      Distance04 = MeasureDistance()
      Distance05 = MeasureDistance()
      Distance06 = MeasureDistance()
      Distance07 = MeasureDistance()
      Distance08 = MeasureDistance()
      Distance09 = MeasureDistance()
      Distance10 = MeasureDistance()
      Distance11 = MeasureDistance()
      Distance12 = MeasureDistance()
      Distance13 = MeasureDistance()
      Distance14 = MeasureDistance()
      Distance15 = MeasureDistance()
      Distance16 = MeasureDistance()
      Distance17 = MeasureDistance()
      Distance18 = MeasureDistance()
      Distance19 = MeasureDistance()
      Distance20 = MeasureDistance()
      Distance_sum = Distance01 + Distance02 + Distance03 + Distance04 + Distance05 + Distance06 + Distance07 + Distance08 + Distance09 + Distance10 + Distance11 + Distance12 + Distance13 + Distance14 + Distance15 + Distance16 + Distance17 + Distance18 + Distance19 + Distance20
      Distance = round(Distance_sum / 20,1)
#    Meine Tanks haben Maximal 3.200 Liter bei 120 cm Füllhöhe
#    Zusätzlich 7 cm Offset vom Einbauort des Sensors; 
      Fuelstand = 127 - Distance
      Liter = 3200 / 120 * Fuelstand
      Zeit = time.time()
      ZeitStempel = datetime.datetime.fromtimestamp(Zeit).strftime('%Y-%m-%d_%H:%M:%S')
      print (ZeitStempel),("Entfernung: %.1f cm" % Distance),(" Fuelhoehe: %.1f cm" % Fuelstand),(" Liter: %.0f l" % Liter)
      time.sleep(.1)

      Auslesezeitpunkt = datetime.datetime.fromtimestamp(Zeit).strftime('%d-%m-%Y_%H:%M:%S')
      Tag = datetime.datetime.fromtimestamp(Zeit).strftime('%Y-%m-%d')
      Uhr = datetime.datetime.fromtimestamp(Zeit).strftime('%H:%M:%S')

	# schreibe Langzeitmessung in *.csv Datei
      file = open("longtimelog.csv", "a")
      file.write(str(Auslesezeitpunkt))
      file.write(", ")
      file.write(str(Distance))
      file.write(" cm, ")
      file.write(str(Fuelstand))
      file.write(" cm, ")
      file.write(str(Liter))
#      file.write(str(Tag))
#      file.write(", ")
#      file.write(str(Liter))
      file.write(" Liter\n")
      file.close()

        # schreibe aktuelle Messung in *.csv Datei
      file = open("log.csv", "w")
      file.write(str(Tag))
      file.write(", ")
      file.write(str(Liter))
      file.write("\n")
      file.close()

      print("Logs aktualisiert")
      time.sleep(.1)
      print("Upload Logs auf FTP...")

        # Lädt die longtimelog.csv Datei auf das NAS
      try:
          filename = "longtimelog.csv"
          ftp = ftplib.FTP(ftpserver)
          ftp.login(ftpuser, ftppassword)
          ftp.cwd(ftppath)
      except:
          print ("*** Keine Verbindung zum FTP-Server !!! ***")
          file = open("connection.csv", "a")
          file.write(str(Auslesezeitpunkt))
          file.write(", ")
          file.write(str(Distance))
          file.write(" cm, ")
          file.write(str(Fuelstand))
          file.write(" cm, ")
          file.write(str(Liter))
#          file.write(str(Tag))
#          file.write(", ")
#          file.write(str(Liter))
          file.write(" Liter")
          file.write("   -   Keine Verbindung zum FTP!\n")
          file.close()
      else:
          os.chdir(r"/home/pi")
          myfile = open("longtimelog.csv", 'r')
          ftp.storlines('STOR ' + "longtimelog.csv", myfile)
          myfile.close()

        # Lädt die log.csv Datei auf das NAS
      try:
          filename = "log.csv"
          ftp = ftplib.FTP(ftpserver)
          ftp.login(ftpuser, ftppassword)
          ftp.cwd(ftppath)
      except:
          print ("*** Keine Verbindung zum FTP-Server !!! ***")
      else:
          os.chdir(r"/home/pi")
          myfile = open("log.csv", 'r')
          ftp.storlines('STOR ' + "log.csv", myfile)
          myfile.close()

      time.sleep(.1)

      print("Verbinde mit MySQL-Datenbank...")

	# Schreibt das Log in die MySQL Datenbank
      try:
          connection = mysql.connector.connect(host = sqlhost, port = sqlport, user = sqluser, passwd = sqlpassword, db = sqldb)
      except:
          print ("*** Keine Verbindung zum MySQL-Server !!! ***")
      else:
          cursor = connection.cursor()
          cursor.execute("INSERT INTO Volumen VALUES (%s,%s)", (Tag,Liter,))
          cursor.close()
          connection.commit()

      time.sleep(.1)

      print("Upload erfolgreich")

  # reset GPIO settings if user pressed Ctrl+C
  except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()

if __name__ == '__main__':
  # use GPIO pin numbering convention
  GPIO.setmode(GPIO.BCM)

  # set up GPIO pins
  GPIO.setup(GPIOTrigger, GPIO.OUT)
  GPIO.setup(GPIOEcho, GPIO.IN)

  # set trigger to false
  GPIO.output(GPIOTrigger, False)

  # call main function
  main()
