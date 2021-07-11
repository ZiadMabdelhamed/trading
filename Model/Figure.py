import json

class Figure :
    data:any
    layout:any

    def __init__(self):
        self.data = []
    def getData(self):
        return self.data

    def setData(self,data):
        self.data = data

    def getLayout(self):
        return self.layout

    def setLayout(self,layout):
        self.layout = layout

