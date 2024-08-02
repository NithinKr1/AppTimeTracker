import time
import psutil
import re
import logging
from flask import Flask, jsonify
from threading import Thread
from PIL import Image
import pygetwindow as gw
import win32process
import win32gui
from titlecase import titlecase
from flask_cors import CORS
from datetime import datetime

class ScreenActivityTracker:
    def __init__(self):
        self.process_time = {}
        self.timestamp = {}
        self.do_run = True
        self.daily_usage = {str(i).zfill(2): 0 for i in range(24)}


    def get_active_window_title(self):
        try:
            active_window = gw.getActiveWindow()
            return active_window.title
        except Exception as e:
            logging.error(f"Error getting active window title: {e}")
            return None

    def track_activity(self, sleep_time):
        '''Track the active window and the time spent on it.'''
        while self.do_run:
            try:
                current_app = psutil.Process(win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]).name().replace(".exe", " ")
                current_app = current_app.replace('ApplicationFrameHost', '')
                current_window_title = self.get_active_window_title()

                self.timestamp[current_app + current_window_title] = int(time.time())
                time.sleep(sleep_time)
                if current_app + current_window_title not in self.process_time:
                    self.process_time[current_app + current_window_title] = 0

                self.process_time[current_app + current_window_title] += int(time.time()) - self.timestamp[current_app + current_window_title]

                parts = re.split(' - | — ', current_window_title)
                for part in parts:
                    part = titlecase(part)
                    if part not in self.process_time:
                        self.process_time[part] = 0
                    self.process_time[part] += int(time.time()) - self.timestamp[current_app + current_window_title]
            except Exception as e:
                logging.error(f"Error tracking activity: {e}")

    def get_sorted_process_time(self):
        '''Return the process time in descending order.'''
        sorted_process_time = {k: v for k, v in sorted(self.process_time.items(), key=lambda item: item[1], reverse=True)}
        return jsonify(sorted_process_time)

    def get_data(self):
        total_usage = sum(self.process_time.values())
        most_used_apps = sorted(self.process_time.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_usage': total_usage // 60,  # Convert to minutes
            'hourly_usage': list(self.daily_usage.values()),
            'most_used_apps': [{'name': app, 'duration': time // 60} for app, time in most_used_apps]
        }

    def update_daily_usage(self):
        current_hour = datetime.now().strftime('%H')
        self.daily_usage[current_hour] = sum(self.process_time.values()) // 60  # Convert to minutes

def create_app(tracker):
    app = Flask(__name__)
    CORS(app)

    @app.route('/data', methods=['GET'])
    def get_data():
        return jsonify(tracker.get_data())

    return app

if __name__ == "__main__":
    import argparse 
    # Setting up sleep time and port number to the argument
    parser = argparse.ArgumentParser(description='Track screen activity.')
    parser.add_argument('--sleep_time', type=int, default=1, help='The time to sleep between checks for the active window.')
    parser.add_argument('--port', type=int, default=5000, help='The port to run the Flask app on.')
    args = parser.parse_args()

    logging.basicConfig(filename='screen_activity_tracker.log', level=logging.INFO)

    # Create a ScreenActivityTracker instance 
    tracker = ScreenActivityTracker()
    tracking_thread = Thread(target=tracker.track_activity, args=(args.sleep_time,))
    tracking_thread.daemon = True
    tracking_thread.start()
    
    def update_usage():
        while True:
            tracker.update_daily_usage()
            time.sleep(1)  # Update every second

    update_thread = Thread(target=update_usage)
    update_thread.daemon = True
    update_thread.start()

    app = create_app(tracker)
    app.run(port=args.port)