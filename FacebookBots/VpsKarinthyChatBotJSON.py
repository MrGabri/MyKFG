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

thread_id = '1571931486208120'
thread_type = ThreadType.GROUP

Weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

url = "https://admin.karinthy.hu/api/substitutions?day="

HWPath = "../Datas/"


email, password = LoadCredentials.LoadCreds()
client = Client(email, password)

with open(HWPath + "schedule.json") as ScheduleFile:
    Schedule = json.load(ScheduleFile)



def GetSubstitutions(_url, day, _class, _lesson, _subject):
    if day.month < 10:
        _month = "0" + str(day.month)
    else:
        _month = day.month
    if day.day < 10:
        _day = "0" + str(day.day)
    else:
        _day = day.day
    url = _url + str(day.year) + "-" + str(_month) + "-" + str(_day)
    r = requests.get(url)
    json_file = r.content
    json_file = json_file.decode('utf8').replace("'", '"')
    data = json.loads(json_file)
    if data != None:
        for index, item in enumerate(data['substitutions']):
            if item['lesson'] == _lesson:
                if item['class'] == _class or item['class'] == '9.ABEC':
                    if item['subject'] == _subject:
                        return item
    return False


def checkHWValidDate():
    date = HWLib.FormatDate()
    for a in HWLib.GetHW():
        if a["nextLessonDate"] is not None:
            if a["nextLessonDate"] == date:
                HWLib.delFromJSON(a["id"])
    return None


def setMessage(_lesson, _subs):
    if _subs == False:
        if not _lesson["start"] == "":
            if "+" in _lesson["start"]:
                msg = ("{} a {} teremben {} -val/vel ami {} percel kesobb kezdodik!".format(_lesson["name"], _lesson["room"],_lesson["teacher"], _lesson["start"])).encode('utf-8')
            if "-" in _lesson["start"]:
                msg = ("{} a {} teremben {} -val/vel ami {} percel elobb kezdodik!".format(_lesson["name"], _lesson["room"],_lesson["teacher"], _lesson["start"])).encode('utf-8')
        else:
            msg = ("{} a {} teremben {} -val/vel!".format(_lesson["name"], _lesson["room"],_lesson["teacher"])).encode('utf-8')

    elif _subs['comment'] == "hazamegy" or _subs['comment'] == "könyvtár":
        msg = ("{}, helyettesites miatt elmarad..., comment: {}".format(_subs["lesson"], _subs['comment'])).encode('utf-8')
    else:
        msg = ("{}, helyettesites miatt a {} teremben {} -val/vel! (Comment: {} )".format(_lesson["name"], _subs["room"] , _subs["substitutingTeacher"], _subs["comment"] )).encode('utf-8')
    return msg


while True:
    f = date.today()
    day = calendar.day_name[f.weekday()]
    now = datetime.now()
    if day == "Saturday" or day == "Sunday":
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
            #print(now.minute)
            if now.minute == 45:
                try:
                    Lesson = Schedule[day][str(now.hour - 6)]
                    subs = GetSubstitutions(url, now, '9.E', now.hour - 7, Lesson["name"])
                    msg = setMessage(Lesson, subs)
                    client.send(Message(text="A következo ora:"), thread_id=thread_id, thread_type=thread_type)
                    print(msg)
                    client.send(Message(text=msg), thread_id=thread_id, thread_type=thread_type)
                except KeyError as e:
                    print(e)
                    client.send(Message(text="A következo ora:"), thread_id=thread_id, thread_type=thread_type)
                    for i in range(1,7):
                        Lesson = Schedule[day][str(now.hour - 6) + "." + str(i)]
                        subs = GetSubstitutions(url, now, '9.E', now.hour - 7, Lesson["name"])
                        msg = setMessage(Lesson, subs)
                        print(msg)
                        client.send(Message(text=msg), thread_id=thread_id, thread_type=thread_type)
                sleep(60)
            else:
                sleep(60)
client.logout()