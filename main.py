# -*- coding: utf-8 -*-
from test import oranged
import wx
import thread
import sys as LOL
import json
import urllib
import time
import ConfigParser
import matplotlib.pyplot as plt
import datetime


class main(wx.Frame):

    
    def __init__(self,parent,id):
        #Creates the window#
        wx.Frame.__init__(self,parent,id, 'BTC PRICE',size=(205,150))
        self.frame = wx.Panel(self)

        #The Settings button#
        self.click = wx.Button(self.frame, label="S", pos=(155,30), size=(30,30))

        #The Chart button#
        chart_button = wx.Button(self.frame, label="Chart", pos=(100,75), size=(70,30))

        self.find_path='config_thing.ini'
        #Binding the button and X to their functions when clicked#
        self.Bind(wx.EVT_BUTTON, self.button, self.click)
        self.Bind(wx.EVT_CLOSE, self.close_window)
        self.Bind(wx.EVT_BUTTON, self.chart_maker, chart_button)

        #Textbox for the bitcoin price#
        self.bitcoin_price = wx.TextCtrl(self.frame,pos=(5,32),size=(140,40),style = wx.NO_BORDER | wx.TE_READONLY)#So the thread stops when the program is closed#

        #Font for the Text box#
        font1 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL)

        #Sets the font to the text box#
        self.bitcoin_price.SetFont(font1)

        #Init the ConfigParser
        self.Config = ConfigParser.ConfigParser()

        #Dictionary of the three currency symbols#
        self.dictionary = {"USD":'$', "GBP": u"\u00A3", "EUR":u"\u20AC"}
        ops_for_charts=['1 Week', '1 Month', '3 Months', '1 Year']
        self.dictionary_for_charts={'1 Week':7, '1 Month':30,'3 Months':90,'1 Year':365}

        self.charting_ops=wx.ComboBox(self.frame,choices=ops_for_charts,pos=(20,78),size=(75,50),style=wx.CB_READONLY)
        #Starts the thread for finding and applying the bitcoin price#
        thread.start_new_thread(self.updater,())

    #Function for calling the Settings Python file#    
    def button(self,event):
        
        windows = oranged(parent=None, id=-1)
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
            price_dict = json.load(urllib.urlopen("http://api.coindesk.com/v1/bpi/currentprice.json"))
            self.do_not_ping=True

            #Gets the currency found in the config file#
            self.the_currency = self.Config.get("settings","currency")

            #Decides whether the price is higher or lower then before so it can change the color of the background#
            if prices > price_dict["bpi"][self.the_currency]["rate"]:
                self.frame.SetBackgroundColour(wx.RED)
                self.bitcoin_price.SetBackgroundColour(wx.RED)
            elif prices < price_dict["bpi"][self.the_currency]["rate"]:
                self.frame.SetBackgroundColour(wx.GREEN)
                self.bitcoin_price.SetBackgroundColour(wx.GREEN)
            else:
                self.frame.SetBackgroundColour(wx.WHITE)
                self.bitcoin_price.SetBackgroundColour(wx.WHITE)

            #Gets the price from api info#
            prices = price_dict["bpi"][self.the_currency]["rate"]

            #Takes the price and puts the currency symbol in front of it#
            priced = self.dictionary[self.the_currency]+prices

            #Sets the textbox to the current bitcoin price#
            self.bitcoin_price.SetValue(priced)

            #Refreshes the window so the background color takes affect#
            self.Refresh()
            self.do_not_ping=False

            #Waits X seconds before looping again#
            time.sleep(float(self.Config.get("settings","refresh")))

    #Makes the chart from the dropdown menu#
    def chart_maker(self,event):
        #Todays date#
        end_date=datetime.date.today()

        #Uses a dictionary to find the amount of days and then finds the date with datetime.timedelta#
        start_date=end_date-datetime.timedelta(days=self.dictionary_for_charts[self.charting_ops.GetValue()])

        #Makes sure there isn't a ping overload so the program doesn't crash#
        if self.do_not_ping==True:
            time.sleep(.2)

        #Gets the chart data from coindesk#
        price_history = json.load(urllib.urlopen("https://api.coindesk.com/v1/bpi/historical/close.json?currency="+self.the_currency+'&start='+str(start_date)+'&end='+str(end_date)))['bpi']

        #Starts the list#
        price_data=[]
        

        #Since the data comes in a dictionary, the prices need to be separated from the dates so I can graph it#
        for i in price_history:
            price_data.append(price_history[i])

        #Plots, labels, and  shows the data#
        plt.plot(price_data)
        plt.ylabel('Price')
        plt.xlabel('Days')
        plt.show()
        
    #Makes sure the threads are done when you click to close the window#        
    def close_window(self,event):
        
        LOL.exit()

#Just some things so the program will run and show the window#
if __name__ =="__main__":
    app = wx.App(False)
    window = main(parent=None, id=-1)
    window.Show()
    app.MainLoop()
    

