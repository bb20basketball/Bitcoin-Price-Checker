import wx
class oranges(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id, 'TEST',size=(500,500))
        self.frams=wx.Panel(self)
        #The unfinished settings#
        another_button=wx.Button(self.frams, label="CLICK ME", pos=(50,50), size=(40,100))
