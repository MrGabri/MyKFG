# -*- coding: utf-8 -*-
from bottle import run, template, route, request, static_file, redirect
from datetime import date, datetime
import calendar
import csv, json
import time, random
from hashids import Hashids
hashids = Hashids()


#Path vars
HWPath = "../HomeWorks/"
TTPath = "../Datas/"
TPLPath = "./Templates/"

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
    with open(HWPath + "Homeworks.json") as infile:
        try: 
            result = json.load(infile)
        except:
            result = []
        return result


#Routeok
@route('/HWAdd')
def admin():
    return template(TPLPath + 'adminform', lessons=GetLessons())

@route('/login')
def loginForm():
    return template(TPLPath + 'login.tpl')

@route('/loginData', method='POST')
def login():
    pw = request.forms.get('pw')
    if pw == "infocsop":
        redirect('/admin')
    else:
        redirect('')


@route('/getData', method='POST')
def getDatas():
    lessons = request.forms.get('selector')
    hw = request.forms.get('hw')
    customDate = request.forms.get('customDate')
    print(lessons + ":" + hw)
    print(customDate)
    saveHW(lessons, hw, customDate)
    redirect('/admin')

@route('/saveData', method='POST')
def saveData():
    hw = request.forms.get('hw')
    customDate = request.forms.get('customDate')
    id = request.forms.get('id')
    print(hw)
    print(customDate)
    changeJSON(hw, customDate, id)
    redirect('/admin')

@route('/changeData', method='POST')
def ChData():
    change = request.forms.get('Change')
    remove = request.forms.get('Remove')
    id = request.forms.get('id')

    hws = GetHW()
    for a in hws:
        if a['id'] == id:
            hw = a
            break

    if change is not None:
        return template(TPLPath + 'changeForm.tpl', less=hw['Lesson'], hw=hw['HW'], cd=hw['nextLessonDate'], id=id)
    if remove is not None:
        delFromJSON(id)
        print("deleted")
        redirect('admin')

@route('/admin')
def HWForm():
    return template(TPLPath + 'HWForm.tpl', homeworks=GetHW())

@route('/')
def HWForm():
    return template(TPLPath + 'index.tpl', homeworks=GetHW())

run(host='37.221.213.41', port=80)
