from bs4 import BeautifulSoup
from Country import  Country
import requests
#Los comentarios en este codigo pueden ser removidos al implementar el paralelismo
countries = []
main_url = "https://www.cia.gov/library/publications/resources/the-world-factbook/"

def getCountryCodes():

    r = requests.get(main_url)
    data = r.text
    soup = BeautifulSoup(data)

    for link in soup.find_all('option'):
        code = link.get('value')
        if(code != ''):
            url = str(main_url)+str(code)
            country = Country(url)
            countries.append(country)



def getCountryPPP():
    for country in countries:
        print('/////////////////////////////////////////////////////////////')
        print(country.url)
        request = requests.get(country.url)
        data = request.text
        soup = BeautifulSoup(data)
        try:
            div1 = soup.find(id="field-gdp-per-capita-ppp")

            div2 = div1.find(class_="category_data subfield historic")

            ppp = div2.find(class_="subfield-number")
            country.setPPP(ppp.text)
        except:
            country.setPPP(0)
        print(country.ppp)

def getCountryMobileAccess():
    for country in countries:
        print('/////////////////////////////////////////////////////////////')
        print(country.url)
        request = requests.get(country.url)
        data = request.text
        soup = BeautifulSoup(data)
        try:
            div1 = soup.find(id="field-telephones-mobile-cellular")

            div2 = div1.find(class_="category_data subfield numeric")

            access = div2.find(class_="subfield-number")

            country.setMobileAccess(access.text)
        except:
            country.setMobileAccess(0)

        print(country.mobileAccess)

def getCountryInternet():
    for country in countries:
        print('/////////////////////////////////////////////////////////////')
        print(country.url)
        request = requests.get(country.url)
        data = request.text
        soup = BeautifulSoup(data)
        try:
            div1 = soup.find(id="field-internet-users")

            div2 = div1.find(class_="category_data subfield numeric")

            subs = div2.find(class_="subfield-number")

            country.setInternetSubs(subs.text)
        except:
            country.setInternetSubs(0)

        print(country.internetSubs)