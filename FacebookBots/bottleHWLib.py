# -*- coding: utf-8 -*-
from datetime import date, datetime
import calendar
import csv, json
import time, random
from hashids import Hashids
hashids = Hashids()


#Path vars
HWPath = "./HomeWorks/"
TTPath = "./Datas/"
DBFile = "./homework.db"

#List vars
Weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
TimeTable = []
todayLessons = []


class HomeWork:
  def __init__(self, date, nextLessonDate, hw, lesson, id):
    self.date = date
    self.nextLessonDate = nextLessonDate
    self.hw = hw
    self.lesson = lesson
    self.id = id

for i in range(0, Weekdays.__len__()): #Load timetable from .csv files
        with open (TTPath + Weekdays[i] + ".csv", 'rb') as f:
            reader = csv.reader(f)
            TimeTable.append(map(tuple, reader))

def GetLessons():
    todayLessons = []
    f = date.today()
    day = calendar.day_name[f.weekday()]
    try:
        dayIndex = Weekdays.index(day)
    except:
        dayIndex = 0
    for i in range(list(TimeTable[dayIndex]).__len__()):
        _less = str(TimeTable[dayIndex][i][0])
        if _less in todayLessons:
            pass
        else:
            if "Masodik" in _less:
                todayLessons.append("Orosz")
                todayLessons.append("Német1")
                todayLessons.append("Német2")
                todayLessons.append("Spanyol1")
                todayLessons.append("Francia")
            else:
                todayLessons.append(_less)
    return todayLessons

def getNewHWID():
    t1 = time.time()
    t2 = t1 + random.randint(1, 200)
    id = hashids.encode(int(t2))
    return id


def FormatDate():
    day = datetime.now()
    if day.month < 10:
        _month = "0" + str(day.month)
    else:
        _month = day.month
    if day.day < 10:
        _day = "0" + str(day.day)
    else:
        _day = day.day
    return str(day.year) + "-" + str(_month) + "-" + str(_day)

def changeJSON(_hw, _customDate, _id):
    with open(HWPath + "Homeworks.json") as infile:
        feed = json.load(infile)
        
    for a in feed:
        if a['id'] == _id:
            a['HW'] = _hw
            if _customDate == "":
                a['nextLessonDate'] = None
            else:
                a['nextLessonDate'] = _customDate
            break

    with open(HWPath + "Homeworks.json", 'w') as outfile:
        json.dump(feed, outfile)

def delFromJSON(_id):
    with open(HWPath + "Homeworks.json") as infile:
        feed = json.load(infile)

    newFeed = [hw for hw in feed if hw['id'] is not _id]
    newFeed = []
    for a in feed:
        if a['id'] != _id:
            print(a)
            newFeed.append(a)

    with open(HWPath + "Homeworks.json", 'w') as outfile:
        json.dump(newFeed, outfile)

def saveHW(_lessons, _hw, _customDate):
    _ID = getNewHWID()
    print(_ID)
    Date = FormatDate()
    if _customDate != "":
        hw = HomeWork(Date, _customDate, _hw, _lessons, _ID)
    else:
        hw = HomeWork(Date, None, _hw, _lessons, _ID)
    hwDict = {}
    hwDict["Date"] = hw.date
    hwDict["nextLessonDate"] = hw.nextLessonDate
    hwDict["HW"] = hw.hw
    hwDict["Lesson"] = hw.lesson
    hwDict["id"] = hw.id
    #print(hwDict)
    with open(HWPath + "Homeworks.json") as infile:
        try:
            feed = json.load(infile)
        except:
            feed = []
    with open(HWPath + "Homeworks.json", 'w') as outfile:
        feed.append(hwDict)
        json.dump(feed, outfile)
    
def GetHW():
    with open("./HomeWorks/Homeworks.json") as infile:
        try: 
            result = json.load(infile)
        except:
            result = []
        return result