import os
import speech_recognition as sr
import webbrowser as wb
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
import time
import tkinter
import threading

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