import time
from datetime import date,datetime
from astral import LocationInfo
from astral.sun import sun

class CamLocation:
    def __init__(self,lat,lon,info,country,timezone):
        self.info = LocationInfo(info, country, timezone, lat, lon)

    def is_night(self):
        s = sun(self.info.observer, date=date.today(),tzinfo=self.info.timezone)

        sunrise = s["sunrise"].timestamp()
        sunset = s["sunset"].timestamp()

        time_now = datetime.now().timestamp()

        if time_now > sunrise and time_now < sunset:
            return False
        else: 
            return True
