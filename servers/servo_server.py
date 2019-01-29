import RPi._GPIO as GPIO
import time
import socket
import sys
import signal


#Initialisation du Server
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 15554

buffer_size = 256




#Initialisation du Servo-Moteur
GPIO.cleanup()
servoPIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO PIN for PWM with 50Hz
p.start(0) # Initialization

# Captation des Signaux
def close(signal, frame):
    #close socket
    serverSocket.close()
    #close and clean gpio
    p.stop()
    GPIO.cleanup()
    print 'SIG:'+ signal + 'Program Interupted'

signal.signal(signal.SIGINT, close)
signal.signal(signal.SIGTERM, close)
signal.signal(signal.SIGQUIT, close)
signal.signal(signal.SIGTSTP, close)

#######---MAIN---#######
if __name__=='__main__':

    try:
        serverSocket.bind((host, port))
    except socket.error as msg:
        print 'Bind fail : ' +str(msg[0]) + 'MESSAGE= '+ msg[1]
        sys.exit()


    while True:
        serverSocket.listen(10)
    	clientSocket, address = serverSocket.accept()
    	angle = clientSocket.recv(buffer_size)
        angle = angle.decode()
        angle = int(angle)/10 + 5

        try:
            p.ChangeDutyCycle(angle)
            time.sleep(0.5)
        except:
            print 'Change Duty cycle FAIL'
            sys.exit()
