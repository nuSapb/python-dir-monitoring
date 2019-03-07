import sys
import time
import logging
import requests
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler



def postData(feederId) :
    url = 'http://localhost:8088/update_pm'
    data = {"feederId": feederId}
    response = requests.post(url, data=data)


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        fname = event.src_path
        result = fname.split('\\')
        data = result[5]
        rawfeederId = data.split('.')
        rawfeederId2 = rawfeederId[0].split('_')
        feederId = rawfeederId2[0]
        if(feederId):
            print(feederId)
            postData(feederId)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    log_handler = LoggingEventHandler()
    event_handler = MyHandler()
    observer = Observer()
    observer2 = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer2.schedule(log_handler, path, recursive=True)

    observer.start()
    observer2.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer2.stop()
    observer.join()
    observer2.join()