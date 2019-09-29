from Bot import *
from Country import *


    
getCountryCodes()

option = int(input(""" Digite la opción de ejecución a realizar
             - 1. Secuencial
             - 2. Paralelo             
              """))
param = int(input(""" Digite la opción del parametro a filtrar
             - 1. PPP
             - 2. Mobile Access
             - 3. Internet             
              """)) 

if (option ==1 and param == 1):
    getCountryPPP()
if (option ==1 and param == 2):
    getCountryMobileAccess()
if (option ==1 and param == 3):
    getCountryInternet()
    
    
    
if (option ==2 and param == 1):
    parallelSearchPPP()
if (option ==2 and param == 2):
    parallelSearchMobileAccess()
if (option ==2 and param == 3):
    parallelSearchInternet()
