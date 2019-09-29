class Country:
#en esta clase se estructuran los datos consultados y necesarios para la graficacion

    def __init__(self,url):
        self.url = url
        self.name=""
        self.ppp = 0
        self.mobileAccess = 0
        self.internetSubs = 0

    def setName(self,name):
        self.name = name
        
    def setPPP(self,ppp):
        self.ppp = ppp

    def setMobileAccess(self,mobileAccess):
        self.mobileAccess = mobileAccess
    def setInternetSubs(self,subs):
        self.internetSubs = subs