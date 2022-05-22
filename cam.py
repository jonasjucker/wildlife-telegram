import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import os
import logging
#from brightpi import *

from subprocess import call

class WildCam:

    def __init__(self):

        self.pin = 24
        self.ir_light_1 = 25
        self.ir_light_2 = 8

        #self.brightPi = BrightPi()

        self.lens = PiCamera()
        self.lens.rotation = 180
        self.lens.resolution=(1024,720)

        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.setup(self.ir_light_1,GPIO.OUT)
        GPIO.setup(self.ir_light_2,GPIO.OUT)

        self.is_recording = False

    def close(self):
        self.lens.close()


    def test(self,name_generator):
        logging.info('Test camera setup')
        photo_day = self.shot(nr_of_shots=1,pause=4,night_mode=False,name_generator=name_generator)
        video_day = self.record(4,night_mode=False,name_generator=name_generator)
        photo_night = self.shot(nr_of_shots=1,pause=4,night_mode=True,name_generator=name_generator)
        video_night = self.record(4,night_mode=True,name_generator=name_generator)

        photos = photo_day + photo_night
        videos = video_day + video_night

        return photos,videos


    def vision_settings(self,is_night):
        if self.is_recording:
            GPIO.output(self.ir_light_1,GPIO.LOW)
            GPIO.output(self.ir_light_2,GPIO.LOW)

            #self.brightPi.set_led_on_off(LED_IR, OFF)
            #self.brightPi.reset()

            self.is_recording = False

        else:
            self.is_recording = True
            if is_night:
                GPIO.output(self.pin,GPIO.LOW)
                GPIO.output(self.ir_light_1,GPIO.HIGH)
                GPIO.output(self.ir_light_2,GPIO.HIGH)

                #self.brightPi.set_led_on_off(LED_IR, ON)
                #self.brightPi.set_gain(15)

                # needed during night for camera to adjust
                time.sleep(1.8)
            else:

                GPIO.output(self.pin,GPIO.HIGH)


    def preview(self,duration, night_mode=False):

        self.vision_settings(night_mode)

        self.lens.start_preview()
        time.sleep(duration)
        self.lens.stop_preview()
        self.vision_settings(night_mode)

    def record(self,duration, night_mode=False,name_generator=None):

        record = []
        self.vision_settings(night_mode)

        record_name = name_generator('h264','v')
        record_mp4 = name_generator('mp4','v')
        self.lens.start_recording(record_name)
        time.sleep(duration)
        self.lens.stop_recording()
        self.vision_settings(night_mode)


        # Convert the h264 format to the mp4 format.
        command = "MP4Box -add " + record_name + " " + record_mp4
        call([command], shell=True)
        logging.info("MP4Box => Video Converted!")

        record.append(record_mp4)

        return record

    def shot(self,nr_of_shots=1,pause=5,night_mode=False,name_generator=None):

        self.vision_settings(night_mode)

        shots_taken = []
        for idx in range(1,nr_of_shots+1):
            record_name = name_generator('jpg','p')
            self.lens.capture(record_name)
            logging.info(f'Shot {idx} taken')
            time.sleep(pause/10.0)
            shots_taken.append(record_name)

        self.vision_settings(night_mode)

        return shots_taken
