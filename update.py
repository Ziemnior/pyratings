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

    if hours_form_ratio + hour_now >= 24 or minutes_form_ratio + minute_now >= 60:
        hour = (hours_form_ratio + hour_now) % 24
        additional_hour_from_minutes = (minutes_form_ratio + minute_now) // 60
        minute = (minutes_form_ratio + minute_now) % 60
        hour += additional_hour_from_minutes
    else:
        hour = hour_now + hours_form_ratio
        minute = minute_now + minutes_form_ratio


def check_for_updates():
    while True:
        date = datetime.now()
        hour_now = int(date.hour)
        minute_now = int(date.minute)

        #print(str(hour_now) + ':' + str(minute_now))
        if hour_now == hour and minute_now == minute:
            print('time to update!')
            set_update_time()
            update()
        else:
            pass

    # replace with infinite loop
    # threading.Timer(15, check_for_updates).start()


# get latest porcys review and pass it to variable
def newest_porcys_url_imported():
    porcys_url_ = get_porcys_review_url()
    porcys_url = porcys_url_[0]
    return porcys_url


# get latest pitchfork review and pass it to variable
def newest_pitchfork_url_imported():
    pitchfork_url_ = get_pitchfork_review_url()
    pitchfork_url = pitchfork_url_[0]
    return pitchfork_url


def update():
    # retrieve var from newest_porcys_url_imported
    first_porcys_url = newest_porcys_url_imported()

    # retrieve var from newest_pitchfork_url_imported
    first_pitchfork_url = newest_pitchfork_url_imported()

    # fetch newest review url with get_porcys_review_url
    get_latest_porcys_url_ = get_porcys_review_url()
    get_latest_porcys_url = get_latest_porcys_url_[0]

    # fetch newest review url with get_pitchfork_review_url
    get_latest_pitchfork_url_ = get_pitchfork_review_url()
    get_latest_pitchfork_url = get_latest_pitchfork_url_[0]

    a = first_porcys_url + ' ' + get_latest_porcys_url
    b = first_pitchfork_url + ' ' + get_latest_pitchfork_url

    get_datetime = datetime.now()
    hour = str(get_datetime.hour)
    minutes = str(get_datetime.minute)

    f = open('log.txt', 'a')
    f.write(hour + ':' + minutes + ' ' + a + '  ' + b + '\n')
    f.close()
    if first_porcys_url != get_latest_porcys_url or first_pitchfork_url != get_latest_pitchfork_url:
        print('new reviews')
        return True
    else:
        pass
        return False


def main():
    set_update_time()
    check_for_updates()

main()