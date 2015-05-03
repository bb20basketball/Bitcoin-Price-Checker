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
        #Creates the window#
        wx.Frame.__init__(self,parent,id, 'BTC PRICE',size=(205,150))
        self.frame=wx.Panel(self)

        #The Settings button#
        self.click=wx.Button(self.frame, label="S", pos=(155,30), size=(30,30))

        #Allowing the program to find the config file on other computers, it is still broken because if you move it, it will break it#
        self.find_path=expanduser('~')
        self.find_path=os.path.join(self.find_path+"\\Downloads\\Bitcoin-Price-Checker-master\\Bitcoin-Price-Checker-master",'config_thing.ini')

        #Binding the button and X to their functions when clicked#
        self.Bind(wx.EVT_BUTTON,self.button, self.click)
        self.Bind(wx.EVT_CLOSE, self.close_window)

        #Textbox for the bitcoin price#
        self.bitcoin_price=wx.TextCtrl(self.frame,pos=(5,32),size=(140,50),style = wx.NO_BORDER | wx.TE_READONLY)#So the thread stops when the program is closed#

        #Font for the Text box#
        font1 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL)

        #Sets the font to the text box#
        self.bitcoin_price.SetFont(font1)

        #Init the ConfigParser
        self.Config=ConfigParser.ConfigParser()

        #Dictionary of the three currency symbols#
        self.dictionary={"USD":'$',"GBP": u"\u00A3","EUR":u"\u20AC"}

        #Starts the thread for finding and applying the bitcoin price#
        thread.start_new_thread(self.updater,())

    #Function for calling the Settings Python file#    
    def button(self,event):
        
        windows=oranged(parent=None, id=-1)
        windows.Show()

    #The main function which finds the price and applies it in the textbox#   
    def updater(self):
        
        #Just the placeholder for the price variable so there isn't an error#
        prices = 0

        #Probably should change the while loop to something better#
        while 1:

            #reads the file for the configs#
            self.Config.read(self.find_path)
            
            #gets api info#
            price_dict=json.load(urllib.urlopen("http://api.coindesk.com/v1/bpi/currentprice.json"))

            #Gets the currency found in the config file#
            the_currency=self.Config.get("settings","currency")

            #Decides whether the price is higher or lower then before so it can change the color of the background#
            if prices > price_dict["bpi"][the_currency]["rate"]:
                self.frame.SetBackgroundColour(wx.RED)
                self.bitcoin_price.SetBackgroundColour(wx.RED)
            elif prices < price_dict["bpi"][the_currency]["rate"]:
                self.frame.SetBackgroundColour(wx.GREEN)
                self.bitcoin_price.SetBackgroundColour(wx.GREEN)
            else:
                self.frame.SetBackgroundColour(wx.WHITE)
                self.bitcoin_price.SetBackgroundColour(wx.WHITE)

            #Gets the price from api info#
            prices=price_dict["bpi"][the_currency]["rate"]

            #Takes the price and puts the currency symbol in front of it#
            priced=self.dictionary[the_currency]+prices

            #Sets the textbox to the current bitcoin price#
            self.bitcoin_price.SetValue(priced)

            #Refreshes the window so the background color takes affect#
            self.Refresh()

            #Waits X seconds before looping again#
            time.sleep(float(self.Config.get("settings","refresh")))

    #Makes sure the threads are done when you click to close the window#        
    def close_window(self,event):
        
        LOL.exit()

#Just some things so the program will run and show the window#
if __name__ =="__main__":
    app=wx.App(False)
    window=main(parent=None, id=-1)
    window.Show()
    app.MainLoop()
    

