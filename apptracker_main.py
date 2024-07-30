from flask import Flask, jsonify
from threading import Thread
import time
import win32process
import win32gui
import psutil
import pygetwindow as gw
import re
from collections import OrderedDict
import logging
import heapq
import argparse
from titlecase import titlecase

class ScreenActivityTracker:
    def __init__(self):
        self.process_time = {}
        self.timestamp = {}

    def get_active_window_title(self):
        try:
            active_window = gw.getActiveWindow()
            return active_window.title
        except Exception as e:
            logging.error(f"Error getting active window title: {e}")
            return None

    def track_activity(self, sleep_time):
        while True:
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
        sorted_process_time = {k: v for k, v in sorted(self.process_time.items(), key=lambda item: item[1], reverse=True)}
        return jsonify(sorted_process_time)

def create_app(sleep_time):
    app = Flask(__name__)
    tracker = ScreenActivityTracker()

    @app.route('/data', methods=['GET'])
    def get_data():
        return tracker.get_sorted_process_time()

    return app, tracker, sleep_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Track screen activity.')
    parser.add_argument('--sleep_time', type=int, default=1, help='The time to sleep between checks for the active window.')
    parser.add_argument('--port', type=int, default=5000, help='The port to run the Flask app on.')
    args = parser.parse_args()

    logging.basicConfig(filename='screen_activity_tracker.log', level=logging.INFO)

    app, tracker, sleep_time = create_app(args.sleep_time)
    tracking_thread = Thread(target=tracker.track_activity, args=(sleep_time,))
    tracking_thread.daemon = True
    tracking_thread.start()
    app.run(port=args.port)
