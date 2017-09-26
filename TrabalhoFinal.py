from gpiozero import MotionSensor
from picamera import PiCamera
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import smtplib

sensor = Adafruit_DHT.DHT11
camera = PiCamera()
camera.rotation = 180
camera.resolution = (2592, 1944)
camera.framerate = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
pir = MotionSensor(pin=25)
pino_sensor = 17

while(True):
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)
    print("Temperatura = {0:0.1f} Umidade = {1:0.1f}").format(temp, umid)
    temperatura = ("{0:0.1f}").format(temp)
    umidade = ("{0:0.1f}").format(umid)
    time.sleep(1)
    
    if(pir.motion_detected and float(temperatura) > 20):
        GPIO.output(4, 1)
        camera.annotate_text_size = 160
        camera.annotate_text = ("Temperatura = {0:0.1f} Umidade = {1:0.1f}").format(temp, umid)
        camera.capture('/home/pi/Documents/image.jpg')
        enviaEmail('/home/pi/Documents/image.jpg')
    else:
        GPIO.output(4, 0)

def enviaEmail(attachment):
    msg = MIMEMultipart('related')
    msg['To'] = ''
    msg['From'] = ''
    msg['Subject'] = 'Teste Email python'

    msgText = MIMEText('<b>teste</b><br><img src="cid:%s"><br>' % (attachment), 'html')
    msg.attach(msgText)

    fp = open(attachment, 'rb')
    img = MIMEImage(fp.read(), 'jpg')
    fp.close
    img.add_header('Content-ID', '<{}>'.format(attachment))
    img.add_header('Content-Disposition', 'inline', filename='image.jpg')
    msg.attach(img)

    #Conexao para enviar o email
    smtp = smtplib.SMTP()
    smtp.connect('smtp.live.com:587')
    smtp.ehlo()
    smtp.starttls()
    smtp.login('usuario','senha')
    smtp.sendmail('De', 'Para', msg.as_string())
    smtp.quit

    print msg.as_string()
    exit(0)
