import configparser
from datetime import datetime
from porcys import get_porcys_review_url
from pitchfork import get_pitchfork_review_url
import wx
from wx import adv
import threading
import os


CONFIG_FILE = 'config.ini'

global current_dir

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# with open(CONFIG_FILE, 'w') as configfile:
#     config.read(configfile)
if os.path.isfile(CONFIG_FILE):
    ratio = config.getint('refresh', 'interval')
else:
    config.add_section('refresh')
    config.set('refresh', 'interval', str(1))
    with open(CONFIG_FILE, 'w+') as configfile:
        config.write(configfile)
    ratio = config.getint('refresh', 'interval')


def show_notification_porcys():
    notification_bubble = wx.App()
    wx.adv.NotificationMessage("", "sample notification porcys").Show()
    notification_bubble.MainLoop()


def show_notification_pitchfork():
    notification_bubble = wx.App()
    wx.adv.NotificationMessage("", "sample notification pitchfork").Show()
    notification_bubble.MainLoop()

def update():

    #get links from config file - if file exists, just pass them, if not - create empty string
    if os.path.isfile(CONFIG_FILE):
        porcys_url = config.get('review links', 'porcys')
        pitchfork_url = config.get('review links', 'pitchfork')
        with open(CONFIG_FILE, 'w+') as configfile:
            config.write(configfile)
    else:
        porcys_url = ""
        pitchfork_url = ""


    # fetch newest review url with get_porcys_review_url
    get_latest_porcys_url_ = get_porcys_review_url()
    get_latest_porcys_url = get_latest_porcys_url_[0]

    # fetch newest review url with get_pitchfork_review_url
    get_latest_pitchfork_url_ = get_pitchfork_review_url()
    get_latest_pitchfork_url = get_latest_pitchfork_url_[0]

    a = porcys_url + ' ' + get_latest_porcys_url
    b = pitchfork_url + ' ' + get_latest_pitchfork_url

    get_datetime = datetime.now()
    hour = str(get_datetime.hour)
    minutes = str(get_datetime.minute)


    if porcys_url != get_latest_porcys_url:
        config.set('review links', 'porcys', porcys_url)
        with open(CONFIG_FILE, 'w+') as configfile:
            config.write(configfile)
        print('new reviews on porcys')

        notification_daemon = threading.Thread(target=show_notification_porcys)
        notification_daemon.daemon = True
        notification_daemon.start()

        f = open('log.txt', 'a')
        f.write(hour + ':' + minutes + ' ' + a + '  ' + b + '\n')
        f.close()

        return True
    elif pitchfork_url != get_latest_pitchfork_url:
        config.set('review links', 'pitchfork', pitchfork_url)
        with open(CONFIG_FILE, 'w+') as configfile:
            config.write(configfile)
        print('new reviews on pitchfork')

        notification_daemon = threading.Thread(target=show_notification_pitchfork)
        notification_daemon.daemon = True
        notification_daemon.start()

        f = open('log.txt', 'a')
        f.write(hour + ':' + minutes + ' ' + a + '  ' + b + '\n')
        f.close()

        return True

    else:
        print('nothing new')
        pass
        return False


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

        if hour_now == hour and minute_now == minute:
            print('time to update!')
            set_update_time()
            update()
        else:
            pass


def run_update():
    set_update_time()
    check_for_updates()