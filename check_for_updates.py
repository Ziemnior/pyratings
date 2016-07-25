import configparser
from datetime import datetime

CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

with open(CONFIG_FILE, 'w') as configfile:
    config.write(configfile)
ratio = config.getint('refresh', 'interval')


def convert_print_date():
    global hour
    global minute
    global hours
    global minutes
    global date_to_check

    hours = ratio//60
    minutes = ratio % 60
    print('updated every '+ str(hours) + 'h ' + str(minutes) + 'm')

    date_ = datetime.now()
    hour = int(date_.hour)
    minute = int(date_.minute)
    print("current time " + str(hour) + ':' + str(minute))

    if hour+hours > 24 or minute + minutes > 60:
        new_day_hour = (hour + hours) % 24
        next_hour_minutes = (minute + minutes) % 60
        next_hour = (minute + minutes) // 60
        new_day_hour += next_hour
        print('update time: ' + str(new_day_hour) + ':' + str(next_hour_minutes))
    else:
        hour += hours
        minute += minutes
        print('update time: ' + str(hour) + ':' + str(minute))



convert_print_date()