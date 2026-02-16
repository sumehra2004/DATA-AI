from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess
import sys
import os

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py"):
            print("Changed:", event.src_path)
            subprocess.run([sys.executable, os.path.join("pipeline", "pipeline.py")])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), path="app", recursive=True)
    observer.start()
    print("👀 Monitoring 'app/' for changes... Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
