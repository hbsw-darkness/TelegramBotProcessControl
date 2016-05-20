#-*- coding: utf-8 -*-
import telebot
from telebot import types
import os, sys
import threading,time
from win32com.client import GetObject
import pythoncom
import datetime

chat_id = "your chat_id"
text = "process stop"

TOKEN = "your token value"

tb = telebot.TeleBot(TOKEN)

#your process checking start command 
@tb.message_handler(commands=['check'])
def send_welcome(message):
    tb.send_message(chat_id, "checking start.")
  
    global processCheck

    processCheck = True

    processName = "processname"
    
    #서버 프로그램 체크 변수
    global processCheckBool
    processCheckBool=False

    while processCheck:
        #이거 써줘야 제대로 프로세스 불러오면서 스레드가 동작한다. 문서 더 찾아봐야
        pythoncom.CoInitialize()
        WMI = GetObject('winmgmts:')
        processes = WMI.InstancesOf('Win32_Process')
        
        for process in processes:
            if process.Properties_('Name').Value == "processName":
                processCheckBool = True
                break
            else:
                processCheckBool = False
                processCheck = False

        if processCheckBool == True:
            processCheck = True
        
        if processCheck == False:
            #When you send a message by telegram of the process is shutdown
            print "not processes"
            tb.send_message(chat_id, text)
            processCheck = False
            break
        #process lise reset
        processes = []

        #제대로 체킹중인지 확인
        print datetime.datetime.now(), "process check"
        time.sleep(10)
        
@tb.message_handler(commands=['stop'])
def send_welcome(message):
    global processCheck
    processCheck = False
    print datetime.datetime.now(), "process check stop"
    tb.send_message(chat_id, "process check")
tb.polling()


