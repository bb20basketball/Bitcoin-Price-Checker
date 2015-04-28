import wx
import sys as LOL
import ConfigParser
class oranged(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id, 'TEST',size=(200,200))
        self.frams=wx.Panel(self)
        #The unfinished settings#
        save=wx.Button(self.frams, label="Save", pos=(50,120), size=(100,30))
        self.Bind(wx.EVT_BUTTON, self.saver, save)
        self.currency=["EUR", "USD","GBP"]
        self.timing=['1','2','3','4','5','6','7','8','9','10']
        one=wx.StaticText(self.frams,-1,"Refresh Rate(Seconds)",pos=(10,30))
        two=wx.StaticText(self.frams,-1,"Currency",pos=(10,75))
        self.Configs=ConfigParser.ConfigParser()
        self.Configs.read("C:\\Users\\Joshua\\Desktop\\config_thing.ini")
        self.adding=wx.ComboBox(self.frams,choices=self.currency,pos=(130,75),size=(50,50),style=wx.CB_READONLY)
        self.time=wx.ComboBox(self.frams,choices=self.timing,pos=(130,30),size=(50,50),style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.get_stuff,self.time)
        self.Bind(wx.EVT_COMBOBOX, self.get_stuff,self.adding)
        self.adding.SetValue(self.Configs.get("settings","currency"))
        self.time.SetValue(self.Configs.get("settings","refresh"))
        #Need a way to call the read function so it doesn't keep opening the file
        #Looking for changes#
    def saver(self,event):
        config_file=open("C:\\Users\\Joshua\\Desktop\\config_thing.ini","w")
        self.Configs.set("settings","refresh", str(self.time.GetValue()))
        self.Configs.set("settings","currency", str(self.adding.GetValue()))
        self.Configs.write(config_file)
        config_file.close()
        self.Destroy()
    def get_stuff(self,event):
        pass
        
