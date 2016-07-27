import configparser
from datetime import datetime
import threading
from porcys import get_porcys_review_url
from pitchfork import get_pitchfork_review_url

CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

with open(CONFIG_FILE, 'w') as configfile:
    config.write(configfile)
ratio = config.getint('refresh', 'interval')


def set_update_time():

    global hours_form_ratio
    global minutes_form_ratio

    global hour
    global minute

    global hour_now
    global minute_now

    hours_form_ratio = ratio//60
    minutes_form_ratio = ratio % 60

    date = datetime.now()
    hour_now = int(date.hour)
    minute_now = int(date.minute)

    if hours_form_ratio + hour_now > 24 or minutes_form_ratio + minute_now > 60:
        hour = (hours_form_ratio + hour_now) % 24
        additional_hour_from_minutes = (minutes_form_ratio + minute_now) // 60
        minute = (minutes_form_ratio + minute_now) % 60
        hour += additional_hour_from_minutes
    else:
        hour = hour_now +  hours_form_ratio
        minute = minute_now + minutes_form_ratio
        if minute == 60:
            minute = 0

def check_for_updates():
    date = datetime.now()
    hour_now = int(date.hour)
    minute_now = int(date.minute)

    print(str(hour_now) + ':' + str(minute_now))
    if hour_now == hour and minute_now == minute:
        print( 'time to update!' )
        set_update_time()
    else:
        pass
    threading.Timer(15,check_for_updates).start()

set_update_time()
check_for_updates()
