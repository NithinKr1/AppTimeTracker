import webview
import threading
import MainAppTracker
import time

def update_html(window):
    while True:
        html = '<html><body><h1>Process Time</h1><p>{}</p></body></html>'.format(MainAppTracker.process_time)
        window.load_html(html)
        time.sleep(1)

window = webview.create_window('MainAppTracker')
threading.Thread(target=update_html, args=(window,)).start()
webview.start()
