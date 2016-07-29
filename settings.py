from tkinter import *
import winreg
import configparser
import os


def settings():
    app = Tk()

    app.maxsize(250, 230)
    app.minsize(250, 230)
    app.title("Settings")
    app.resizable(0, 0)

    # path to startup on Windows
    REGISTRY_PATH = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"
    CONFIG_FILE = 'config.ini'
    current_dir = os.path.abspath(__file__)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # adding value to register
    def add_to_startup():
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, 'pyRatings', 0, winreg.REG_SZ, current_dir)
            key.Close()
        except Exception:
            pass
        information.config(text="Successfully added to startup.")

    # deleting value from register
    def delete_from_startup():
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0,
                                 winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY)
            winreg.DeleteValue(key, 'pyRatings')
            key.Close()
        except Exception:
            pass
        information.config(text="Successfully removed form startup.")

    # save interval to config file
    def save_refresh_ratio():
        if not os.path.isfile(CONFIG_FILE):
            config.add_section('refresh')
            config.set('refresh', 'interval', str(refresh_scale.get()))
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
        else:
            config.set('refresh', 'interval', str(refresh_scale.get()))
            with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)
        ratio = config.getint('refresh', 'interval')
        current_interval.config(text="(current interval: "+str(ratio)+')')

    startup_frame = LabelFrame(app, text="Startup")
    startup_frame.pack(side=TOP, fill="both", expand="yes")

    add = Button(startup_frame, text="Add to startup", command=add_to_startup)
    delete = Button(startup_frame, text="Delete from startup", command=delete_from_startup)
    information = Label(startup_frame, text="")

    add.pack()
    delete.pack()
    information.pack()

    refresh_frame = LabelFrame(app, text="Refresh ratio")
    refresh_frame.pack(side=TOP, fill="both", expand="yes")

    if os.path.isfile(CONFIG_FILE):
        ratio = config.getint('refresh', 'interval')
    else:
        ratio = 0

    refresh_label = Label(refresh_frame, text="Check for updates every X minutes: ")

    current_interval = Label(refresh_frame, text="(current interval: "+str(ratio)+')')

    refresh_scale = Scale(refresh_frame, from_=0, to=720, resolution=10, length=300, orient=HORIZONTAL, variable=ratio)

    save = Button(refresh_frame, text='Save', command=save_refresh_ratio)

    refresh_label.pack()
    current_interval.pack()
    refresh_scale.pack()
    save.pack()

    app.iconbitmap(r'images/icon.ico')
    app.mainloop()