# -*- coding: utf-8 -*-
from fbchat import Client
from fbchat.models import *
from datetime import datetime, date
import csv
import calendar
from time import sleep, gmtime, strftime
from decimal import Decimal
import json
import pprint
import requests
import sqlite3
import bottleHWLib as HWLib
import LoadCredentials



#thread_id = '1571931486208120' #Main mode
thread_id = '1599731243462067'  #Dev mode
thread_type = ThreadType.GROUP

Weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

url = "https://admin.karinthy.hu/api/substitutions?day={}"

TTPath = "../Datas/"


email, password = LoadCredentials.LoadCreds()
client = Client(email, password) #Login to facebook

with open(TTPath + "schedule.json") as ScheduleFile: #Load schedule file
    Schedule = json.load(ScheduleFile)


def GetSubstitutions(day, _class, _lesson, _subject):
    r = requests.get(url.format(date.today().isoformat()))
    json_file = r.content
    json_file = json_file.decode('utf8').replace("'", '"')
    data = json.loads(json_file)
    if data != None:
        for index, item in enumerate(data['substitutions']):
            if item['lesson'] == _lesson:
                if item['class'] == _class or item['class'] == '9.ABEC':
                    if item['subject'].lower() == _subject.lower():
                        return item
    return False


def checkHWValidDate():
    date = HWLib.FormatDate()
    for a in HWLib.GetHW():
        if a["nextLessonDate"] is not None:
            if a["nextLessonDate"] == date:
                HWLib.delFromJSON(a["id"])
    return None


msgAlap = "{} a {} teremben {} -val/vel!"
msgElobb = "{} a {} teremben {} -val/vel ami {} percel elobb kezdodik!"
msgKesobb = "{} a {} teremben {} -val/vel ami {} percel kesobb kezdodik!"
msgElmarad = "{}, helyettesites miatt elmarad...(Comment: {})"
msgHelyettesites = "{}, helyettesites miatt a {} teremben {} -val/vel! (Comment: {} )"

def setMessage(_name, _lesson, _subs):
    if _subs == False:
        if not _lesson["start"] == "":
            if "+" in _lesson["start"]:
                msg = (msgKesobb.format(_name, _lesson["room"],_lesson["teacher"], _lesson["start"])).encode('utf-8')
            if "-" in _lesson["start"]:
                msg = (msgElobb.format(_name, _lesson["room"],_lesson["teacher"], _lesson["start"])).encode('utf-8')
        else:
            msg = (msgAlap.format(_name, _lesson["room"],_lesson["teacher"])).encode('utf-8')

    elif _subs['comment'] == "hazamegy" or _subs['comment'] == "könyvtár":
        msg = (msgElmarad.format(_name, _subs['comment'])).encode('utf-8')
    else:
        msg = (msgHelyettesites.format(_name, _subs["room"] , _subs["substitutingTeacher"], _subs["comment"] )).encode('utf-8')
    return msg


def printLesson(now):
    for name, data in Schedule[now.weekday()][now.hour - 6].items(): # iterate through next lesson(s)
        subs = GetSubstitutions(now, '9.E', now.hour - 6, name) # get substitutions for next lesson
        msg = setMessage(name, data, subs) # get motd
        client.send(Message(text="A következö ora:"), thread_id=thread_id, thread_type=thread_type)
        print(msg)
        client.send(Message(text=msg), thread_id=thread_id, thread_type=thread_type)


while True:
    now = datetime.now()
    if 5 <= now.weekday():
        print("sleep for 6h")
        sleep(14400)
    else:
        if now.hour <= 7:
            print("sleep for 15m")
            sleep(900)
        elif now.hour >= 14:
            checkHWValidDate()
            print("sleep for 1h")
            sleep(3600)
        else:
            if now.minute == 45:
                printLesson(now)
            sleep(60)
client.logout()