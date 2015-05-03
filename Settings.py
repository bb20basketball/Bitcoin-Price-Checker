import wx
import sys as LOL
import ConfigParser

#This is the class for the settings#
class oranged(wx.Frame):
    
    def __init__(self,parent,id):

        #Makes the window#
        wx.Frame.__init__(self,parent,id, 'Settings',size=(200,200))
        self.frams=wx.Panel(self)

        #Creates and binds the save button#
        save=wx.Button(self.frams, label="Save", pos=(50,120), size=(100,30))
        self.Bind(wx.EVT_BUTTON, self.saver, save)

        #Defines the list of possible currency#
        self.currency=["EUR", "USD", "GBP"]
        
        #Path of the config file#
        self.find_paths='config_thing.ini'

        #List of time.sleeps#
        self.timing=['1','2','3','4','5','6','7','8','9','10']

        #Label for the dropdowns#
        one=wx.StaticText(self.frams,-1,"Refresh Rate(Seconds)",pos=(10,30))
        two=wx.StaticText(self.frams,-1,"Currency",pos=(10,75))

        #Init of the Config Parser#
        self.Configs=ConfigParser.ConfigParser()

        #Reads the Config file so it can preset the dropdowns#
        self.Configs.read(self.find_paths)

        #Starts the dropdowns#
        self.adding=wx.ComboBox(self.frams,choices=self.currency,pos=(130,75),size=(50,50),style=wx.CB_READONLY)
        self.time=wx.ComboBox(self.frams,choices=self.timing,pos=(130,30),size=(50,50),style=wx.CB_READONLY)

        #Sets the dropdowns to the value the user set#
        self.adding.SetValue(self.Configs.get("settings","currency"))
        self.time.SetValue(self.Configs.get("settings","refresh"))
        #Need a way to call the read function so it doesn't keep opening the file
        #Looking for changes#

    #Takes the input and then saves it to a file#
    def saver(self,event):

        #Opens the config file and it will write to it#
        config_file=open(self.find_paths,"w")

        #Sets the new settings#
        self.Configs.set("settings","refresh", str(self.time.GetValue()))
        self.Configs.set("settings","currency", str(self.adding.GetValue()))

        #Writes the config settings#
        self.Configs.write(config_file)

        #Close the file#
        config_file.close()

        #Closes the window and returns to the main window#
        self.Destroy()

        
