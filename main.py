import RPi.GPIO as GPIO

from sensors import Pir
from cam import WildCam

def main():

    GPIO.setmode(GPIO.BCM)

    pir = Pir()
    pir.activate()

    cam = WildCam()

    try:
        while True:
            pir.wait_for_movement()
            cam.shot(nr_of_shots=3,pause=1,night_mode=True)
            cam.record(3,night_mode=True)

    except KeyboardInterrupt:
        cam.close()
        GPIO.cleanup()
        print('Cleanup')




if __name__ == '__main__':
    main()
