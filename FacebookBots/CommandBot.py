# -*- coding: utf-8 -*-
from fbchat import log, Client
from fbchat.models import *
import time
import json
import LoadCredentials

email, password = LoadCredentials.LoadCreds()
HWPath = "../HomeWorks/"
homeworks = []

class Msg():
    def __init__(self, author_id, message_object, thread_id, thread_type):
        self.author_id = author_id
        self.message_object = message_object
        self.thread_id = thread_id
        self.thread_type = thread_type

class CustomClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsRead(thread_id)
        if author_id != self.uid:
            gotMessage(self, author_id, message_object, thread_id, thread_type, **kwargs)



def ReadHWJson(msgData):
    with open("./HomeWorks/Homeworks.json") as infile:
        result = json.load(infile)
    for hw in result:
        print(hw)
        msg = str(hw["Lesson"]) + ", " + str(hw["HW"])
        client.send(Message(text=str(msg)), msgData.thread_id, msgData.thread_type)

def ClearJson(msgData):
    with open(HWPath + "Homeworks.json", 'w') as outfile:
        outfile.write("")
    client.send(Message(text="JSON File cleared!"), msgData.thread_id, msgData.thread_type)

def HelloWorld(msgData):
    users = client.fetchAllUsers()
    for user in users:
        if user.uid == msgData.author_id:
            client.send(Message(text="Hello, " + user.name), msgData.thread_id, msgData.thread_type)
            return None
    client.send(Message(text="Hello World!"), msgData.thread_id, msgData.thread_type)
    return None

def HelloAdmin(msgData):
    users = client.fetchAllUsers()
    for user in users:
        if user.uid == msgData.author_id:
            client.send(Message(text="Hello, " + user.name + "(Admin)"), msgData.thread_id, msgData.thread_type)
            return None
    client.send(Message(text="Hello World!"), msgData.thread_id, msgData.thread_type)
    return None

def GetAdmins():
    admins = []
    with open('admins.ad', 'r') as a_file:
        line = a_file.readline()
        while line:
            admins.append(int(line))
            line = a_file.readline()
    return admins

def NoYou(msgData):
    client.send(Message(text="No u!"), msgData.thread_id, msgData.thread_type)

def ShowHelp(msgData):
    msg = """
    *Commands:* 
> ❓ or ".help"
 *to show help*
> 📚 or ".show_homeworks"
 *to show homeworks*
> 👋 or ".hello bot"
 *to greet the bot*
> 💾 or ".link"
 *to show link to the webpage*
    """
    client.send(Message(text=msg), msgData.thread_id, msgData.thread_type)

def AddAdmin(msgData):
    add, name = msgData.message_object.text.split("@")
    users = client.fetchAllUsers()
    for user in users:
        if user.name == name:
            with open('admins.ad', 'a+') as a_file:
                a_file.write(user.uid + '\n')

def SendLink(msgData):
    client.send(Message(text="http://37.221.213.41/"), msgData.thread_id, msgData.thread_type)

admincommands = {
    ".clear_json": ClearJson,
    ".helloBot" : HelloAdmin,
    ".add_admin" : AddAdmin
}

commands = {
    ".show_homeworks": ReadHWJson,
    ".hello bot": HelloWorld,
    ".fuck you bot": NoYou,
    ".help" : ShowHelp,
    ".link" : SendLink,
    "📚" : ReadHWJson,
    "❓" : ShowHelp,
    "👋" : HelloWorld,
    "💾" : SendLink
}


def gotMessage(self, author_id, message_object, thread_id, thread_type, **kwargs): 
    msgData = Msg(author_id, message_object, thread_id, thread_type)
    print(message_object.text.encode("utf-8"))
    if message_object.text.encode("utf-8") in commands:
        print(message_object.text.encode("utf-8"))
        commands[message_object.text.encode("utf-8")](msgData)
    print(GetAdmins())
    print(author_id in GetAdmins())
    if int(author_id) in GetAdmins():
        com = message_object.text.encode("utf-8").split(" ")
        for strings in com:
            if strings in admincommands:
                admincommands[strings](msgData)

client = CustomClient(
    email,
    password)
client.listen()