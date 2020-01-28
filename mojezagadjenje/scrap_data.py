import requests
import json
from bs4 import BeautifulSoup # To get everything
from selenium import webdriver
import time

def getData(URL):
        with requests.session() as client:
            responseGet = client.get(URL)
            return responseGet

def get_cities():
  URL='https://www.fhmzbih.gov.ba/latinica/index.php'
  # Get all data
  response = getData(URL)
  soup = BeautifulSoup(response.text,'html.parser')
  # Get Resultset
  prognoza_div = soup.findAll('div',{"id":"prognoza1"})
  # Get tag type(prognoza_div)
  gradovi= prognoza_div[1]
  # Get again ResulSet
  gradovi = gradovi.find_all('tr')
  #gradovi = soup.select('prognoza table td a') # nadje zadnju
  linkovi={}
  home='https://www.fhmzbih.gov.ba'
  for grad in gradovi:
    # Get tag again -> grad -> get Resultset again->temp
    a = grad.findAll('a')
    if(a):
      linkovi[a[0].text]=[]
      linkovi[a[0].text].append({
        "url":home+a[0]['href']
      })
  return linkovi
# x["Zenica"][0]["url"]

def get_aqi():
  zenica_url=get_cities()["Zenica"][0]["url"]
  print(zenica_url)
  driver = webdriver.Firefox()
  driver.get(zenica_url)
  time.sleep(4)
  soup1 = BeautifulSoup(driver.page_source, 'html.parser')
  div = soup1.findAll('div',class_='newspaper1 meni')
  aqi_link = div[1].findAll('a')[1]['href']
  driver.get(aqi_link)
  # This link could be a starting point in general:
  #http://www.fhmzbih.gov.ba/latinica/ZRAK/AQI-satne.php


def scrap_aqi():
  url='http://www.fhmzbih.gov.ba/latinica/ZRAK/AQI-satne.php'
  response = getData(url)
  soup = BeautifulSoup(response.text,'html.parser')
  div_date = soup.find('div',{"class":"subtitle"}).text
  date1=div_date.replace(u'\xa0', u'')
  date=date1 # temporary variable
  day=int(date[0:date.find('.')])
  date=date[date.find('.')+1:]
  year=int(date[0:date.find('.')])
  date=date[date.find('u')+1:].strip() # remove empty char
  hour= int(date[0:2])
  # Find table - ResultSet:
  table= soup.find('table',{"class":"table"}).findAll('tr')
  x=table
  temp= 0
  lokacije={}
  t=list(range(9,13))
  for j in len(t):
    i=t[j]
    if i==9:
      temp=1
    else:
      temp=0
    lokacija= x[i].findAll('td')[temp].text #brist
    print(lokacija)
    lokacije[lokacija]=[]
    #h2s= x[9].findAll('td')[2].text# zenica don't measure it
    lokacije[lokacija].append({
      "so2":x[i].findAll('td')[temp+1].text,
      "no2":x[i].findAll('td')[temp+2].text,
      "nox":x[i].findAll('td')[temp+3].text,
      "no":x[i].findAll('td')[temp+4].text,
      "co":x[i].findAll('td')[temp+5].text,
      "o3":x[i].findAll('td')[temp+4].text,
      "pm10":x[i].findAll('td')[temp+5].text,
    })
  # Vranduk is special
  lokacija= x[13].findAll('td')[0].text #brist
  lokacije[lokacija]=[]
  #so2= x[9].findAll('td')[2].text # vranduk don't measure
  #h2s= x[9].findAll('td')[2].text# zenica don't measure it
  #no2= x[9].findAll('td')[2].text# vranduk don't measure
  #nox= x[9].findAll('td')[2].text# vranduk don't measure
  #no= x[9].findAll('td')[2].text# vranduk don't measure
  #co= x[9].findAll('td')[2].text# vranduk don't measure
  lokacije[lokacija].append({
    "o3":x[13].findAll('td')[0].text,
    "pm10":x[13].findAll('td')[1].text,
    "pm25":x[13].findAll('td')[2].text
  })
  return lokacije



  
