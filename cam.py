import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import os
import logging

from subprocess import call

class WildCam:

    def __init__(self):

        self.pin = 24
        self.lens = PiCamera()
        GPIO.setup(self.pin,GPIO.OUT)

    def close(self):
        self.lens.close()

    def preview(self,duration, night_mode=False):

        if night_mode:
            GPIO.output(self.pin,GPIO.LOW)
        else:
            GPIO.output(self.pin,GPIO.HIGH)

        self.lens.start_preview()
        time.sleep(duration)
        self.lens.stop_preview()

    def record(self,duration, night_mode=False):

        if night_mode:
            GPIO.output(self.pin,GPIO.LOW)
        else:
            GPIO.output(self.pin,GPIO.HIGH)

        record_name = self.new_record_name('h264','v')
        record_mp4 = self.new_record_name('mp4','v')
        self.lens.start_recording(record_name)
        time.sleep(duration)
        self.lens.stop_recording()

        # Convert the h264 format to the mp4 format.
        command = "MP4Box -add " + record_name + " " + record_mp4
        call([command], shell=True)
        logging.info("\r\nRasp_Pi => Video Converted! \r\n")

        return record_mp4

    def shot(self,nr_of_shots=1,pause=1,night_mode=False):

        if night_mode:
            GPIO.output(self.pin,GPIO.LOW)
        else:
            GPIO.output(self.pin,GPIO.HIGH)

        shots_taken = []
        for idx in range(1,nr_of_shots+1):
            record_name = self.new_record_name('jpg','p')
            self.lens.capture(record_name)
            print(f'Shot {idx} taken')
            time.sleep(pause)
            shots_taken.append(record_name)

        return shots_taken

    def new_record_name(self,suffix,type):
        t = time.localtime()
        timestamp = time.strftime('%Y-%m-%d_%H%M%S', t)


        name = timestamp + "." + suffix 
        if type == 'v':
            name = os.path.join('videos',name)
        elif type == 'p':
            name = os.path.join('photos',name)
        else:
            name = os.path.join('garbage',name)

        return name


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    camtest = WildCam()

    camtest.preview(2,night_mode=True)
    camtest.preview(2)

    camtest.shot(nr_of_shots=2,pause=1,)
    camtest.shot(nr_of_shots=2,pause=1,night_mode=True)

    camtest.record(3)
    camtest.record(3,night_mode=True)

    camtest.close()
    GPIO.cleanup()
