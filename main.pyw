# -*- coding: utf-8 -*-
from Settings import oranged
import wx
import thread
import sys as LOL
import json
import urllib
import time
import ConfigParser
import os
from os.path import expanduser
class main(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id, 'BTC PRICE',size=(205,150))
        self.frame=wx.Panel(self)
        self.click=wx.Button(self.frame, label="S", pos=(155,30), size=(30,30))
        self.find_path=expanduser('~')
        self.find_path=os.path.join(self.find_path+"\\Downloads\\Bitcoin-Price-Checker-master\\Bitcoin-Price-Checker-master",'config_thing.ini')
        self.Bind(wx.EVT_BUTTON,self.button, self.click)
        self.Bind(wx.EVT_CLOSE, self.close_window)
        font1 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.bitcoin_price=wx.TextCtrl(self.frame,pos=(5,32),size=(140,50),style = wx.NO_BORDER | wx.TE_READONLY)#So the thread stops when the program is closed#
        self.bitcoin_price.SetFont(font1)
        self.Config=ConfigParser.ConfigParser()
        self.dictionary={"USD":'$',"GBP": u"\u00A3","EUR":u"\u20AC"}
        thread.start_new_thread(self.updater,())
    def button(self,event):
        windows=oranged(parent=None, id=-1)
        windows.Show()
    def updater(self):
        prices=0
        while 1:
            self.Config.read(self.find_path)
            price_dict=json.load(urllib.urlopen("http://api.coindesk.com/v1/bpi/currentprice.json"))
            the_currency=self.Config.get("settings","currency")
            if prices > price_dict["bpi"][the_currency]["rate"]:
                self.frame.SetBackgroundColour(wx.RED)
                self.bitcoin_price.SetBackgroundColour(wx.RED)
            elif prices < price_dict["bpi"][the_currency]["rate"]:
                self.frame.SetBackgroundColour(wx.GREEN)
                self.bitcoin_price.SetBackgroundColour(wx.GREEN)
            else:
                self.frame.SetBackgroundColour(wx.WHITE)
                self.bitcoin_price.SetBackgroundColour(wx.WHITE)
            prices=price_dict["bpi"][the_currency]["rate"]
            priced=self.dictionary[the_currency]+prices
            self.bitcoin_price.SetValue(priced)
            self.Refresh()
            time.sleep(float(self.Config.get("settings","refresh"))) 
    def close_window(self,event):
        LOL.exit()
if __name__ =="__main__":
    app=wx.App(False)
    window=main(parent=None, id=-1)
    window.Show()
    app.MainLoop()
    

