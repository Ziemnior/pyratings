import wx
from wx import adv

TRAY_TOOLTIP = 'PyRatings'
TRAY_ICON = (r'images/icon.ico')

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'See latest Porcys ratings', self.on_porcys)
        create_menu_item(menu, 'See lates Pitchfork ratings', self.on_pitchfork)
        menu.AppendSeparator()
        create_menu_item(menu, "Settings", self.on_settings)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        pass

    def on_porcys(self, event):
        print('open Porcys reviews')

    def on_pitchfork(self, event):
        print('open Pitchfork reviews')

    def on_settings(self, event):
        print("Open settings")

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()

# dodać powiadmienia o nowych recenzjach - demona