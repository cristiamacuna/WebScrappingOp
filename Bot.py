from bs4 import BeautifulSoup
from Country import  Country
import requests
import matplotlib.pyplot as plt
import time
import threading

#Los comentarios en este codigo pueden ser removidos al implementar el paralelismo
#print("Cantidad de CPU: ", cpu_count())


countries = []
main_url = "https://www.cia.gov/library/publications/resources/the-world-factbook/"
cont=[]

#Metodo recibe la lista de paises ordenados a graficar y el parametro a usar de medicion
def graficar(top,param): 
    plt.figure(figsize=(70, 7))
    plt.subplot(131)
    for c in top:
        plt.bar(c.name, getattr(c, param)  )
    plt.suptitle('TOP por paises')
    plt.show()


#Realiza el ordenamiento para consegui el top de 
def ordenamientoBurbuja(unaLista,param):
    for numPasada in range(len(unaLista)-1,0,-1): 
         for i in range(numPasada):
             if getattr(unaLista[i], param) > getattr(unaLista[i+1], param) :
                 temp = unaLista[i]
                 unaLista[i] = unaLista[i+1]
                 unaLista[i+1] = temp
    return unaLista[::-1]



#Metodo para obtener los codigos de los paises desde el select HTML
def getCountryCodes():
    r = requests.get(main_url)
    data = r.text # Website's HTML
    soup = BeautifulSoup(data,'lxml')
    for link in soup.find_all('option'):
        name= link.text
        code = link.get('value') #Codigo de pais (select HTML)
        if(code != ''):
            url = str(main_url)+str(code)
            country = Country(url)
            country.setName(name)
            countries.append(country)
    print("Paises obtenidos  ... " , len(countries))



def getCountryPPP():
    print("Procesando getCountryPPP")
    for country in countries:
        request = requests.get(country.url)
        data = request.text
        soup = BeautifulSoup(data, "lxml")
        try:
            div1 = soup.find(id="field-gdp-per-capita-ppp")
            div2 = div1.find(class_="category_data subfield historic")
            ppp = div2.find(class_="subfield-number")
            
            pppClear = ppp.text.replace("$","")
            pppInt = int(pppClear.replace(",", ""))
            # $12,500  --> 12500
            country.setPPP(pppInt)
        except:
            country.setPPP(0)
    lista = ordenamientoBurbuja(countries,"ppp")
    graficar(lista[:10],"ppp")


def getCountryMobileAccess():
    print("Procesando getCountryMobileAccess")
    for country in countries:
        request = requests.get(country.url)
        data = request.text
        soup = BeautifulSoup(data,"lxml")
        try:
            div1 = soup.find(id="field-telephones-mobile-cellular")
            div2 = div1.find(class_="category_data subfield numeric")
            access = div2.find(class_="subfield-number").text
            
            accessInt = int(access.replace(",", ""))
            # 12,500  --> 12500
            country.setMobileAccess(accessInt)
        except:
            country.setMobileAccess(0)
        #print(country.mobileAccess)
    lista = ordenamientoBurbuja(countries[:11],"mobileAccess")
    graficar(lista[:10],"mobileAccess")



def getCountryInternet():
    print("Procesando getCountryInternet")
    for country in countries:
        request = requests.get(country.url)
        data = request.text
        soup = BeautifulSoup(data,"lxml")
        try:
            div1 = soup.find(id="field-internet-users")
            div2 = div1.find(class_="category_data subfield numeric")

            subs = div2.find(class_="subfield-number").text
            subsInt = int(subs.replace(",", ""))
            # 12,500  --> 12500
            country.setInternetSubs(subsInt)
        except:
            country.setInternetSubs(0)

    lista = ordenamientoBurbuja(countries[:11],"internetSubs")
    graficar(lista[:10],"internetSubs")
        


############################################# Metodos paralelos


def getCountryPPPParallel(self,country,index):
    request = requests.get(country.url)
    data = request.text
    soup = BeautifulSoup(data, "lxml")
    try:
        div1 = soup.find(id="field-gdp-per-capita-ppp")
        div2 = div1.find(class_="category_data subfield historic")
        ppp = div2.find(class_="subfield-number")
        
        pppClear = ppp.text.replace("$","")
        pppInt = int(pppClear.replace(",", ""))
        # $12,500  --> 12500
        countries[index].setPPP(pppInt)
    except:
        countries[index].setPPP(0)

    cont.append(1)
    if len(cont) == len(countries):
        lista = ordenamientoBurbuja(countries,"ppp")
        print("Dato mayor: ", lista[0].ppp)
        graficar(lista[:10],"ppp")



def getCountryMobileAccessParallel(self,country,index):
    request = requests.get(country.url)
    data = request.text
    soup = BeautifulSoup(data,"lxml")
    try:
        div1 = soup.find(id="field-telephones-mobile-cellular")
        div2 = div1.find(class_="category_data subfield numeric")
        access = div2.find(class_="subfield-number").text
        
        accessInt = int(access.replace(",", ""))
        # 12,500  --> 12500
        country.setMobileAccess(accessInt)
    except:
        country.setMobileAccess(0)
        
    cont.append(1)
    if len(cont) == len(countries):
        lista = ordenamientoBurbuja(countries,"mobileAccess")
        print("Dato mayor: ", lista[0].mobileAccess)
        graficar(lista[:10],"mobileAccess")





def getCountryInternetParallel(self,country,index):
    #for country in countries:
    request = requests.get(country.url)
    data = request.text
    soup = BeautifulSoup(data,"lxml")
    try:
        div1 = soup.find(id="field-internet-users")
        div2 = div1.find(class_="category_data subfield numeric")

        subs = div2.find(class_="subfield-number").text
        subsInt = int(subs.replace(",", ""))
        # 12,500  --> 12500
        countries[index].setInternetSubs(subsInt)
    except:
        countries[index].setInternetSubs(0)
    
    cont.append(1)
    if len(cont) == len(countries):
        lista = ordenamientoBurbuja(countries,"internetSubs")
        print("Dato mayor: ", lista[0].internetSubs)
        graficar(lista[:10],"internetSubs")



def parallelSearchPPP():   
    cont.clear()
    print("Procesando parallelSearchPPP .....")
    size = len(countries)
    for i in range(0,size//2):
        threading.Thread(target=getCountryPPPParallel,args=("",countries[i],i)).start()
    for j in range(size//2,size):
        threading.Thread(target=getCountryPPPParallel,args=("",countries[j],j)).start()
        

def parallelSearchMobileAccess():   
    cont.clear()
    print("Procesando parallelSearchMobileAccess .....")
    size = len(countries)
    for i in range(0,size//2):
        threading.Thread(target=getCountryMobileAccessParallel,args=("",countries[i],i)).start()
    for j in range(size//2,size):
        threading.Thread(target=getCountryMobileAccessParallel,args=("",countries[j],j)).start()
        


def parallelSearchInternet():   
    cont.clear()
    print("Procesando parallelSearchInternet.....")
    size = len(countries)
    for i in range(0,size//2):
        threading.Thread(target=getCountryInternetParallel,args=("",countries[i],i)).start()
    for j in range(size//2,size):
        threading.Thread(target=getCountryInternetParallel,args=("",countries[j],j)).start()
    


    











        
        
        
        