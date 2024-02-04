import speech_recognition as sr
import webbrowser as wb
import os
import winsound
import win32com.client
import re
import requests
from bs4 import BeautifulSoup
import ssdk
import sys
import webbrowser
import win32com.client
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import speech_recognition
import time
import pyaudio
import wave 
import tkinter as tk
import math
import multiprocessing as multi
import mediapipe as mp
import cv2
import numpy as np 
import tkinter
import threading
import playsound
import cv2 as cv
import AiPhile
shell = win32com.client.Dispatch("WScript.Shell") 
r = sr.Recognizer()

def youtube():
    print ("您想搜尋什麼?")
    winsound.PlaySound("audio/google.wav", winsound.SND_FILENAME)
    #winsound.PlaySound("youtube.wav", winsound.SND_FILENAME)
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10,phrase_time_limit=6)
            qq = r.recognize_google(audio,language='zh-TW')
            print("您所說的話: " + qq)
        if 'homepage' in qq:
            wb.open("https://www.youtube.com/?gl=TW&hl=zh-TW")
            winsound.PlaySound("audio/mission.wav", winsound.SND_FILENAME)
        else:  #這裡搜尋所講的話 並且可以選擇要挑哪個網址開啟
            url_you="https://www.youtube.com/results?search_query=" + qq
            wb.open(url_you)
            winsound.PlaySound("audio/mission.wav", winsound.SND_FILENAME)

            # 這邊把搜尋到的結果網址一個一個揪出來
            res = requests.get(url_you , verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            last = None

            myList = []
            for entry in soup.select('a'):  # soup.select('a')得到了很多條網址字串  for每個字串一個一個處理
                m = re.search("v=(.*)", entry['href'])  # 網址篩選條件
                if m:
                    target = m.group(1)  # 這邊引進得到的網址字串
                    if target == last:
                        continue
                    if re.search("list", target):
                        continue
                    last = target
                    myList.append(target)
                    #print(target)

            # def you_film():  # 這個FN是用來選影片  #跟you_film不在同一個 def裡面 因此抓不到def
            #     winsound.PlaySound("audio/choose.wav", winsound.SND_FILENAME)
            #     try:

            #         print("請選擇您要觀看哪一則影片，第一部請說第一部，第二部說第二部以此類推...")
            #         with sr.Microphone() as source:
            #             r.adjust_for_ambient_noise(source)
            #             audio = r.listen(source, timeout=10, phrase_time_limit=5)
            #             choose = r.recognize_google(audio, language='zh-TW')
            #             print("你所說的話: " + choose)
            #             if '一' in choose:
            #                 wb.open("https://www.youtube.com/watch?v=" + myList[0])
            #                 print("https://www.youtube.com/watch?v=" + myList[0])
            #                 print("第一部影片已開啟")

            #             elif '二' in choose:
            #                 wb.open("https://www.youtube.com/watch?v=" + myList[1])
            #                 print("第二部影片已開啟")

            #             elif '三' in choose:
            #                 wb.open("https://www.youtube.com/watch?v=" + myList[2])
            #                 print("第二部影片已開啟")

            #             elif '四' in choose:
            #                 wb.open("https://www.youtube.com/watch?v=" + myList[3])
            #                 print("第二部影片已開啟")

            #             elif '五' in choose:
            #                 wb.open("https://www.youtube.com/watch?v=" + myList[4])
            #                 print("第二部影片已開啟")
            #             elif '關掉' in choose:
            #                 close1()
            #             else:
            #                 print("對不起我沒聽清楚，請再說一次。")
            #                 winsound.PlaySound("audio/again.wav", winsound.SND_FILENAME)
            #                 you_film()

                # except:
                #     print("對不起我沒聽清楚，麻煩再說一次。")
                #     winsound.PlaySound("audio/again.wav", winsound.SND_FILENAME)
                #     you_film()

        you_film()


            #print(myList)
            #you_film()  #執行選影片的fn

    except:
        print("我真的聽不懂抱歉，請再說一次。")
        winsound.PlaySound("audio/again.wav", winsound.SND_FILENAME)
        youtube()

def listt():
    window = tk.Tk()
    window.title('運動健身鏡 App')
    window.geometry('800x250')
    window.configure(background='white')

    header_label = tk.Label(window, text='健身鏡運動結束', font=("Arial", 60, "bold"), padx=5, pady=5, bg="red", fg="yellow")
    header_label.pack()

    a_frame = tk.Frame(window)
    a_frame.pack(side=tk.TOP)
    a_label = tk.Label(a_frame, text='請把器具歸還到原位，歡迎下次使用!!', font=("Arial", 30, "bold"), padx=5, pady=5, bg="white", fg="black")
    a_label.pack(side=tk.LEFT)

    b_frame = tk.Frame(window)
    b_frame.pack(side=tk.TOP)
    b_label = tk.Label(b_frame, text='如要繼續使用，請將此視窗關閉，並繼續說出指令', font=("Arial", 22, "bold"), padx=5, pady=5, bg="white", fg="black")
    b_label.pack(side=tk.LEFT)

    result_label = tk.Label(window)
    result_label.pack()

    lbTime= tkinter.Label(window, fg='red',anchor='w')
    lbTime.place(x=10,y=220,width=150)
    richText = tkinter.Text(window, width=380)

    def autoClose():
        for i in range(10):
            lbTime['text'] = '距離關閉還有{}秒'.format(10-i)
            time.sleep(1)
        window.destroy()

    t=threading.Thread(target=autoClose)
    t.start()

    window.mainloop()

def starttitle():
    window = tk.Tk()
    window.title('運動健身鏡 App')
    window.geometry('1500x600')
    window.configure(background='white')


    header_label = tk.Label(window, text='觀迎使用智慧動作檢測健身鏡', font=("Arial", 80, "bold"), padx=5, pady=5, bg="red", fg="yellow")
    header_label.pack()

    a_frame = tk.Frame(window)
    a_frame.pack(side=tk.TOP)
    a_label = tk.Label(a_frame, text='請依指令直接說出需要的運動項目或者需求!', font=("Arial", 40, "bold"), padx=5, pady=5, bg="white", fg="black")
    a_label.pack(side=tk.LEFT)

    b_frame = tk.Frame(window)
    b_frame.pack(side=tk.TOP)
    b_label = tk.Label(b_frame, text='試著說:彎舉、深蹲、抬舉、飛鳥、Youtube、Google等等', font=("Arial", 40, "bold"), padx=5, pady=5, bg="white", fg="black")
    b_label.pack(side=tk.LEFT)


    d_frame = tk.Frame(window)
    d_frame.pack(side=tk.TOP)
    d_label = tk.Label(d_frame, text='若要將網頁關閉，請直接說出:關掉', font=("Arial", 30, "bold"), padx=5, pady=5, bg="white", fg="black")
    d_label.pack(side=tk.TOP)


    c_frame = tk.Frame(window)
    c_frame.pack(side=tk.TOP)
    c_label = tk.Label(c_frame, text='等運動結束後請說出結束，程式將會直接結束', font=("Arial", 30, "bold"), padx=5, pady=5, bg="white", fg="black")
    c_label.pack(side=tk.TOP)


    result_label = tk.Label(window)
    result_label.pack()


    lbTime= tkinter.Label(window, fg='red',anchor='w')
    lbTime.place(x=10,y=560,width=150)
    richText = tkinter.Text(window, width=380)


    def autoClose():
        for i in range(10):
            lbTime['text'] = '距離關閉還有{}秒'.format(10-i)
            time.sleep(1)
        window.destroy()

    t=threading.Thread(target=autoClose)
    t.start()

    window.mainloop()



def apple():
    print ("您想搜尋什麼?")
    winsound.PlaySound("audio/google.wav", winsound.SND_FILENAME)
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10,phrase_time_limit=6)
            qq = r.recognize_google(audio,language='zh-TW')
            print("您所說的話: " + qq)
        if 'homepage' in qq:
            wb.open("https://www.google.com/?gl=TW&hl=zh-TW")
            winsound.PlaySound("audio/mission.wav", winsound.SND_FILENAME)
        else:  #這裡搜尋所講的話 並且可以選擇要挑哪個網址開啟
            url_you="https://www.google.com.tw/search?q=" + qq
            wb.open(url_you)
            winsound.PlaySound("audio/mission.wav", winsound.SND_FILENAME)
            res = requests.get(url_you, verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            last = None

            myList = []
            for entry in soup.select('a'): 
                m = re.search("v=(.*)", entry['href'])  
                if m:
                    target = m.group(1)  
                    if target == last:
                        continue
                    if re.search("list", target):
                        continue
                    last = target
                    myList.append(target)
    except:
        print("我真的聽不懂抱歉，請再說一次。")
        winsound.PlaySound("audio/again.wav", winsound.SND_FILENAME)
        apple()


def close1():
    browserExe = "chrome.exe"
    os.system("taskkill /f /im " + browserExe)
    print("Chrome已經關閉。")

var = 1

while var == 1:  # 此條件永遠true，將無限循環行下去  可以使用 CTRL+C 來中斷。
    r = sr.Recognizer()


    try:
        with sr.Microphone() as source:
            print("Speak:")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=60,phrase_time_limit=3)

        data = r.recognize_google(audio, language='zh-TW')
        print("您所說的話: " + data )
        if '啟動' in data:
            winsound.PlaySound("audio/sound.wav", winsound.SND_FILENAME)
            winsound.PlaySound("audio/jarvis.wav", winsound.SND_FILENAME)
            winsound.PlaySound("audio/welcome.wav", winsound.SND_FILENAME)
            starttitle()
        elif '播放' in data:
            shell.SendKeys("^%{HOME}", 0)
        elif '下' in data:
            shell.SendKeys("^%{RIGHT}", 0)
        elif '大' in data:
            shell.SendKeys("^%{UP}", 0)
            winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME);winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME)
        elif '小' in data:
            shell.SendKeys("^%{DOWN}", 0)
            winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME);winsound.PlaySound("audio/dong.wav", winsound.SND_FILENAME)
        elif 'facebook' in data or 'Facebook' in data:
            wb.open('https://www.facebook.com/')
        elif '翻譯' in data or '翻' in data:
            wb.open('https://translate.google.com.tw/?hl=zh-TW')
        elif 'YouTube' in data:
            youtube()
        elif '關掉' in data or '關閉' in data:
            close1()
        elif '彎舉' in data or '手臂' in data or '彎曲' in data:
            os.system("python -u ssdkdistancee.py")
        elif '深蹲' in data or '腿' in data:
            os.system("python -u ssek.py")
        elif '抬舉' in data or '深舉' in data:
            os.system("python -u ssgk.py")
        elif '飛鳥' in data or '展臂' in data:
            os.system("python -u ssfk.py")
        elif 'google' in data or 'Google' in data:
            apple()
        elif '完成' in data or '結束' in data:
            winsound.PlaySound("audio/end.wav", winsound.SND_FILENAME)
            os.system("python -u autoclose2.py")
    except sr.UnknownValueError:
        print("有需求的話，請繼續跟我說!")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except:
        pass 