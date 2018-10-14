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
TimeTable = []

url = "https://admin.karinthy.hu/api/substitutions?day="

HWPath = "../Datas/"


email, password = LoadCredentials.LoadCreds()
client = Client(email, password)

for i in range(0, Weekdays.__len__()):
	with open (HWPath + Weekdays[i] + ".csv", 'rb') as f:
            reader = csv.reader(f)
            TimeTable.append(map(tuple, reader))



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
                if item['class'] == _class:
                    if item['subject'] == _subject:
                        return item
        return False



def setMessage(_dayless, _subs):
    if _subs != False:
        if _subs['comment'] == "hazamegy" or _subs['comment'] == "könyvtár":
            msg = "A következő óra helyettesítés miatt elmarad..., comment:" + _subs['comment']
        else:
            msg = ("Next lesson is {} in room{} with{} cause of substitutions! (Comment: {})".format(_dayless[0], _subs['room'], _subs['substituting_teacher'], _subs['comment'])).encode('utf-8')
    else:
        msg = "Next lesson is {} in room{} with{}.".format(DayLess[0], DayLess[1], DayLess[2])
    return msg


def checkHWValidDate():
    date = HWLib.FormatDate()
    for a in HWLib.GetHW():
        if a["nextLessonDate"] is not None:
            if a["nextLessonDate"] == date:
                HWLib.delFromJSON(a["id"])
    return None



while True:
    f = date.today()
    day = calendar.day_name[f.weekday()]
    if day != "Saturday" or day != "Sunday":
        now = datetime.now()
        print("H:" + str(now.hour))
        if 6 < now.hour < 15:
            print(now.minute)
            if now.minute == 45:
                less = now.hour
                less -= 7
                print(TimeTable)
                dayN = Weekdays.index(day)
                print(dayN)
                print(less)
                try:
                    DayLess = TimeTable[dayN][less]
                    subs = GetSubstitutions(url, now, '9.E', less + 1, DayLess[0])
                    try:
                        _less = less - 1
                        if DayLess[0] == TimeTable[dayN][_less]:
                            pass
                        else:
                            msg = setMessage(DayLess, subs)
                            print(msg)
                            messageId = client.send(Message(text=str(msg)), thread_id=thread_id, thread_type=thread_type)
                            client.reactToMessage(messageId, MessageReaction.YES)
                    except:
                        msg = setMessage(DayLess, subs)
                        print(msg)
                        client.send(Message(text=msg), thread_id=thread_id, thread_type=thread_type)
                        client.reactToMessage(messageId, MessageReaction.YES)
                except:
                    pass
                sleep(60)
            else:
                sleep(60)
        elif now.hour <= 7:
            print("sleep for 15m")
            sleep(900)
        elif now.hour >= 15:
            checkHWValidDate()
            print("sleep for 1h")
            sleep(3600)
    else:
        print("sleep for 6h")
        sleep(14400)
client.logout()
