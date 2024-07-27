from win32gui import GetForegroundWindow, GetWindowText
import psutil
import time
import win32process
import pygetwindow as gw
import re
import json
from flask import Flask, jsonify

app = Flask(__name__)

process_time = {}
timestamp = {}

def get_window_info():
    try:
        active_window = gw.getActiveWindow()
        active_window_title = active_window.title
    except Exception:
        active_window_title = None
    return active_window_title

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(process_time)

def track_activity():
    while True:
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", " ")
        current_app = current_app.replace('ApplicationFrameHost', '')
        current_window_title = get_window_info()

        timestamp[current_app + current_window_title] = int(time.time())
        time.sleep(1)
        if current_app + current_window_title not in process_time.keys():
            process_time[current_app + current_window_title] = 0
        
        process_time[current_app + current_window_title] = process_time[current_app + current_window_title] + int(time.time()) - timestamp[current_app + current_window_title]

        parts = re.split(' - | — ', current_window_title)
        for part in parts:
            if part not in process_time.keys():
                process_time[part] = 0
            process_time[part] = process_time[part] + int(time.time()) - timestamp[current_app + current_window_title]

if __name__ == "__main__":
    from threading import Thread
    tracking_thread = Thread(target=track_activity)
    tracking_thread.daemon = True
    tracking_thread.start()
    app.run(port=5000)
