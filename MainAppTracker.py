from win32gui import GetForegroundWindow, GetWindowText
import psutil
import time
import win32process
import pygetwindow as gw
import re

process_time = {}
timestamp = {}

def get_window_info():
    # Get the title of the active window
    try:
        active_window = gw.getActiveWindow()
        active_window_title = active_window.title
    except Exception:
        active_window_title = None

    return active_window_title

while True:
    current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", " ")
    
    #Microoft Store apps always begin with ApplicationFrameHost
    #This will remove the ApplicationFrameHost from the name
    current_app = current_app.replace('ApplicationFrameHost', '')
    
    current_window_title = get_window_info()    
    
    #Timestamp here is used to calculate the time spent on each window using the difference between the current time and the last time the window was active
    timestamp[current_app + current_window_title] = int(time.time())
    time.sleep(1)
    if current_app + current_window_title not in process_time.keys():
        process_time[current_app + current_window_title] = 0
    
    process_time[current_app + current_window_title] = process_time[current_app + current_window_title] + int(time.time()) - timestamp[current_app + current_window_title]
    
    # Splitting the string and assign the time to each part
    parts = re.split(' - | — ', current_window_title)  
    for part in parts:
        if part not in process_time.keys():
            process_time[part] = 0
        process_time[part] = process_time[part] + int(time.time()) - timestamp[current_app + current_window_title]
    
    print(process_time)

