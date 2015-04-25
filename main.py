from test import oranged
import wx
import thread
import sys as LOL
import json
import urllib
import time
import ConfigParser
class main(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id, 'BTC PRICE',size=(200,150))
        self.frame=wx.Panel(self)
        self.click=wx.Button(self.frame, label="S", pos=(150,30), size=(30,30))
        self.Bind(wx.EVT_BUTTON,self.button, self.click)
        self.Bind(wx.EVT_CLOSE, self.close_window)
        font1 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.bitcoin_price=wx.TextCtrl(self.frame,pos=(15,32),size=(120,50),style = wx.NO_BORDER | wx.TE_READONLY)#So the thread stops when the program is closed#
        self.bitcoin_price.SetFont(font1)
        self.Config=ConfigParser.ConfigParser()
        thread.start_new_thread(self.updater,())
    def button(self,event):
        windows=oranged(parent=None, id=-1)
        windows.Show()
        print "somethign"
    def updater(self):
        prices=0
        while 1:
            self.Config.read("C:\\Users\\Joshua\\Desktop\\config_thing.ini")
            price_dict=json.load(urllib.urlopen("http://api.coindesk.com/v1/bpi/currentprice.json"))
            if prices > price_dict["bpi"][self.Config.get("settings","currency")]["rate"]:
                self.frame.SetBackgroundColour(wx.RED)
                self.bitcoin_price.SetBackgroundColour(wx.RED)
            elif prices < price_dict["bpi"][self.Config.get("settings","currency")]["rate"]:
                self.frame.SetBackgroundColour(wx.GREEN)
                self.bitcoin_price.SetBackgroundColour(wx.GREEN)
            else:
                self.frame.SetBackgroundColour(wx.WHITE)
                self.bitcoin_price.SetBackgroundColour(wx.WHITE)
            prices=(price_dict["bpi"][self.Config.get("settings","currency")]["rate"])
            self.bitcoin_price.SetValue(prices)
            self.Refresh()
            time.sleep(float(self.Config.get("settings","refresh"))) #Seems like three is the magic number#
    def close_window(self,event):
        LOL.exit()
if __name__ =="__main__":
    app=wx.App(False)
    window=main(parent=None, id=-1)
    window.Show()
    app.MainLoop()
    

