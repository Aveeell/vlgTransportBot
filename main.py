from bs4 import BeautifulSoup
import requests
import cfg
import emoji
import re


def getPageOfBus(busNumber):
    mainPage = requests.get(cfg.url)
    soup = BeautifulSoup(mainPage.text, 'html.parser')
    soup.find('div', {"class": "contact-user bg-green"})
    bus = soup.find('span', text=busNumber.replace(' ', '').upper())
    href = bus.previous.previous.previous.attrs['href']
    return href


def getPageOfDirections(href):
    directionPage = requests.get(cfg.url + href)
    dirPage = BeautifulSoup(directionPage.text, "html.parser")
    table = dirPage.find('table')
    listOfDirection = table.findAll('a')
    cfg.directions = [listOfDirection[0].text.replace('(А)', '\b'), listOfDirection[1].text.replace('(А)', '\b'),
                      listOfDirection[0].attrs["href"], listOfDirection[1].attrs["href"]]


def chooseDirection(userChoice):
    if userChoice == '1':
        return cfg.directions[2]
    elif userChoice == '2':
        return cfg.directions[3]


def printSchedule(choosenDirection):
    choosenDir = requests.get(cfg.url + choosenDirection)
    timingPage = BeautifulSoup(choosenDir.text, 'html.parser')
    timingTable = timingPage.find('tbody')
    schedule = ''
    for item in timingTable:
        item = item.text
        if item[1].isdigit():
            item = item[1:6] + " " + item[6:]
        schedule += item + "\n"
    return schedule


def getAllBuses():
    mainPage = requests.get(cfg.url)
    soup = BeautifulSoup(mainPage.text, 'html.parser')
    buses = soup.findAll('div', 'contact-user bg-green')
    listOfBuses = []
    for bus in buses:
        listOfBuses.append(bus.text)
    return str(listOfBuses)[1:-1].replace('.', '')


def getAllTrolleybuses():
    mainPage = requests.get(cfg.url)
    soup = BeautifulSoup(mainPage.text, 'html.parser')
    trolleybuses = soup.findAll('div', 'contact-user bg-red')
    listOfTrolleybuses = []
    for trolleybus in trolleybuses:
        listOfTrolleybuses.append(trolleybus.text)
    return str(listOfTrolleybuses)[1:-1].replace('.', '')
