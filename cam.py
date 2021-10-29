import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import os
import logging

from subprocess import call

class WildCam:

    def __init__(self):

        self.pin = 24
        self.ir_light_1 = 25
        self.ir_light_2 = 8

        self.lens = PiCamera()

        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.setup(self.ir_light_1,GPIO.OUT)
        GPIO.setup(self.ir_light_2,GPIO.OUT)

        self.is_recording = False

    def close(self):
        self.lens.close()

    def vision_settings(self,is_night):
        if self.is_recording:
            GPIO.output(self.ir_light_1,GPIO.LOW)
            GPIO.output(self.ir_light_2,GPIO.LOW)
            self.is_recording = False

        else:
            self.is_recording = True
            if is_night:
                GPIO.output(self.pin,GPIO.LOW)
                GPIO.output(self.ir_light_1,GPIO.HIGH)
                GPIO.output(self.ir_light_2,GPIO.HIGH)
            else:
                GPIO.output(self.pin,GPIO.HIGH)


    def preview(self,duration, night_mode=False):

        self.vision_settings(night_mode)

        self.lens.start_preview()
        time.sleep(duration)
        self.lens.stop_preview()
        self.vision_settings(night_mode)

    def record(self,duration, night_mode=False):

        self.vision_settings(night_mode)

        record_name = self.new_record_name('h264','v')
        record_mp4 = self.new_record_name('mp4','v')
        self.lens.start_recording(record_name)
        time.sleep(duration)
        self.lens.stop_recording()
        self.vision_settings(night_mode)


        # Convert the h264 format to the mp4 format.
        command = "MP4Box -add " + record_name + " " + record_mp4
        call([command], shell=True)
        logging.info("MP4Box => Video Converted!")

        return record_mp4

    def shot(self,nr_of_shots=1,pause=1,night_mode=False):

        self.vision_settings(night_mode)

        shots_taken = []
        for idx in range(1,nr_of_shots+1):
            record_name = self.new_record_name('jpg','p')
            self.lens.capture(record_name)
            logging.info(f'Shot {idx} taken')
            time.sleep(pause)
            shots_taken.append(record_name)

        self.vision_settings(night_mode)

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
