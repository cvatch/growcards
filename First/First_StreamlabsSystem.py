#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Redeem script to redeem rewards for a cost for users"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import re
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "First"
Website = "https://www.twitch.tv/must13"
Creator = "Must13"
Version = "1.0.3"
Description = "Reward the first users to show up"
#---------------------------------------
# Versions
#---------------------------------------
""" 
1.0.3 - Added an option to disable the game while stream is Offline. Added an option to have an Offline Message. Added a usercooldown for this Offline Message to prevent spam.
1.0.2 - Replaced the usercooldown by a list of users instead to check who's been rewarded or late. Added a Reset button in the script's UI to play the game again.
1.0.1 - Prevented "winners" from getting other rewards.
1.0.0 - Initial Release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no custom settings file is found
            self.OnlyWhenLive = True
            self.EnableOfflineMessage = True
            self.MessageOfflineStream = "Nice try $user but the stream isn't live :p"
            self.Commands = "!first first"
            self.MessageRewardFirst = "Whooohooo! $user is first and gets $value $currencyname!! PogChamp"
            self.MessageRewardSecond = "Sorry $user. You are not first today but as second you get $value $currencyname!! PogChamp"
            self.MessageRewardThird = "Sorry $user. You are not first today but as third you get $value $currencyname!! PogChamp"
            self.MessageTooLate = "Sorry $user. You were too slow today. FeelsBadMan" 
            self.RewardFirst = 100
            self.RewardSecond = 50
            self.RewardThird = 25
            self.EnableSecond = True
            self.EnableThird = True

    # Reload settings on save through UI
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        """Save settings to files (json and js)"""
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return

#---------------------------------------
# Settings functions
#---------------------------------------
def ReloadSettings(jsondata):
    """Reload settings on Save"""
    # Reload saved settings
    MySet.ReloadSettings(jsondata)
    # End of ReloadSettings

def SaveSettings(self, settingsFile):
    """Save settings to files (json and js)"""
    with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
        json.dump(self.__dict__, f, encoding='utf-8-sig')
    with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
        f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
    return

#---------------------------------------
# System functions
#---------------------------------------

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """data on Load, required function"""
    ResetFirst()
    global MySet
    # Load in saved settings
    MySet = Settings(settingsFile)
    # End of Init
    global firstcommand 
    firstcommand = MySet.Commands.lower().split()
    return

def Execute(data):
    """Required Execute data function"""
    global First
    global Second
    global Third
    global Users
    global FirstUser
    global SecondUser
    global ThirdUser
    if not MySet.EnableSecond:
        Second = True
        Third = True
    if not MySet.EnableThird:
        Third = True
    if data.IsChatMessage() and data.GetParam(0).lower() in firstcommand:
        if not Parent.IsLive() and MySet.OnlyWhenLive:
            if MySet.EnableOfflineMessage:
                if Parent.IsOnUserCooldown(ScriptName, str(firstcommand), data.User):
                    return
                else:
                    SendResp(data, "Stream Chat", MySet.MessageOfflineStream)
                    Parent.AddUserCooldown(ScriptName, str(firstcommand), data.User, 3600)
            return
        if data.UserName in Users:
            return
        if First and Second and Third:
            Message = MySet.MessageTooLate
            Message = Message.replace("$first", FirstUser)
            Message = Message.replace("$second", SecondUser)
            Message = Message.replace("$third", ThirdUser)
            SendResp(data, "Stream Chat", Message)
            Users.append(data.UserName)
        elif not First:
            Parent.AddPoints(data.User,data.UserName,MySet.RewardFirst)
            Message = MySet.MessageRewardFirst
            Message = Message.replace("$value", str(MySet.RewardFirst))
            SendResp(data, "Stream Chat", Message)
            Users.append(data.UserName)
            FirstUser = data.UserName
            First = True
            return
        elif not Second:
            Parent.AddPoints(data.User,data.UserName,MySet.RewardSecond)
            Message = MySet.MessageRewardSecond
            Message = Message.replace("$value", str(MySet.RewardSecond))
            Message = Message.replace("$first", FirstUser)
            SendResp(data, "Stream Chat", Message)
            Users.append(data.UserName)
            SecondUser = data.UserName
            Second = True
            return
        elif not Third:
            Parent.AddPoints(data.User,data.UserName,MySet.RewardThird)
            Message = MySet.MessageRewardThird
            Message = Message.replace("$value", str(MySet.RewardThird))
            Message = Message.replace("$first", FirstUser)
            Message = Message.replace("$second", SecondUser)
            SendResp(data, "Stream Chat", Message)
            Users.append(data.UserName)
            ThirdUser = data.UserName
            Third = True
    return
def Tick():
    """Required tick function"""
    return

#---------------------------------------
# Parse functions
#---------------------------------------

def SendResp(data, Usage, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())

    l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and (Usage in l) and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendStreamWhisper(data.User, Message)

    l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
    if data.IsFromDiscord() and not data.IsWhisper() and (Usage in l):
        Parent.SendDiscordMessage(Message)

    l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
    if data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendDiscordDM(data.User, Message)

#---------------------------------------
# UI functions
#---------------------------------------    
def ResetFirst():    
    """Open the Redeems.txt in the scripts folder"""
    global Users
    global First
    global Second
    global Third
    global FirstUser
    global SecondUser
    global ThirdUser
    First = False
    Second = False
    Third = False
    Users = []
    FirstUser = ""
    SecondUser = ""
    ThirdUser = ""
    return