#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# BCM GPIO-Referenen verwenden (anstelle der Pin-Nummern)
# und GPIO-Eingang definieren
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 23

print ("PIR-Modul gestartet (CTRL-C to exit)")

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)

# Initialisierung
Read  = 0
State = 0
#time.sleep(10)
try:
  print ("Warten, bis PIR im Ruhezustand ist ...")
  time.sleep(10)
  # Schleife, bis PIR == 0 ist
  while GPIO.input(GPIO_PIR) != 0:
    time.sleep(0.1)
  print ("Bereit...")

  # Endlosschleife, Ende mit STRG-C
  while True:
    # PIR-Status lesen
    Read = GPIO.input(GPIO_PIR)

    if Read == 1 and State == 0:
      # PIR wurde getriggert
      print ("Bewegung erkannt!")
      cam = picamera.PiCamera()
      #Foto mit der Kamera machen
      cam.resolution = (640, 480)
      #cam.start_preview()
      #time.sleep(1)
      #cam.stop_preview()
      for i in range (10):
        cam.capture("Bilder/"+"pir"+str(i+1)+".jpg")
        print(i+1)
        time.sleep(1)
        #cam.close()
       	#print(i)
      #time.sleep(5)
      # Zustand merken
      cam.close()
      State = 1
      #Email versenden zur Benachrichtigung
      senderEmail = "t"
      empfangsEmail = ""
      msg = MIMEMultipart()
      msg["From"] = senderEmail
      msg["To"] = empfangsEmail
      msg["Subject"] = "Bewegung erkannt"
    
      emailText = "Es wurde eine Bewegung erkannt"
      msg.attach(MIMEText(emailText, "html"))
    
      server = smtplib.SMTP("smtp.provider.de")
      server.starttls()
      server.login(senderEmail, "")
      text = msg.as_string()
      server.sendmail(senderEmail, empfangsEmail, text)
      server.quit()
    elif Read == 0 and State == 1:
      # PIR wieder im Ruhezustand
      time.sleep(5)
      print ("wieder Bereit...")
      # Zustand merken
      State = 0

    # kleine Pause
      time.sleep(0.1)
      

except KeyboardInterrupt:
  # Programm beenden
  print ("Ende...")
  GPIO.cleanup()
