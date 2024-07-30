import sys
import argparse
import logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from threading import Thread
from apptracker_main import ScreenActivityTracker
from flask import Flask

def create_app(sleep_time):
    app = Flask(__name__)
    tracker = ScreenActivityTracker()

    @app.route('/data', methods=['GET'])
    def get_data():
        return tracker.get_sorted_process_time()

    return app, tracker, sleep_time

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Screen Activity Tracker')
        menu = QMenu(parent)

        start_action = QAction("Start Tracking", parent)
        start_action.triggered.connect(self.start_tracking)
        menu.addAction(start_action)

        stop_action = QAction("Stop Tracking", parent)
        stop_action.triggered.connect(self.stop_tracking)
        menu.addAction(stop_action)

        exit_action = QAction("Exit", parent)
        exit_action.triggered.connect(lambda: sys.exit())
        menu.addAction(exit_action)

        self.setContextMenu(menu)

    def start_tracking(self):
        global tracking_thread
        if not tracking_thread.is_alive():
            tracking_thread = Thread(target=tracker.track_activity, args=(sleep_time,))
            tracking_thread.daemon = True
            tracking_thread.start()

    def stop_tracking(self):
        global tracking_thread
        if tracking_thread.is_alive():
            tracking_thread.join()

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

    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QIcon('apptrackerlogo.png'), w)
    tray_icon.show()
    sys.exit(app.exec_())
