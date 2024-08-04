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

class ScreenActivityTracker:
    def __init__(self):
        self.process_time = {}
        self.timestamp = {}
        self.do_run = True

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

def create_app(tracker):
    '''Create a Flask app to serve the process time data.'''
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    @app.route('/data', methods=['GET'])
    def get_data():
        return tracker.get_sorted_process_time()

    return app

if __name__ == "__main__":
    import argparse 
    # Setting up sleep time and port number to the argument
    parser = argparse.ArgumentParser(description='Track screen activity.')
    parser.add_argument('--sleep_time', type=int, default=1, help='The time to sleep between checks for the active window.')
    parser.add_argument('--port', type=int, default=5000, help='The port to run the Flask app on.')
    args = parser.parse_args()

    # logging.basicConfig(filename='screen_activity_tracker.log', level=logging.INFO)

    # Create a ScreenActivityTracker instance 
    tracker = ScreenActivityTracker()
    tracking_thread = Thread(target=tracker.track_activity, args=(args.sleep_time,))
    tracking_thread.daemon = True
    tracking_thread.start()

    app = create_app(tracker)
    app.run(port=args.port)