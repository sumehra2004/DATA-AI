from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess
import sys
import os

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # ignore noisy changes
        if event.is_directory:
            return
        print("File changed:", event.src_path)
        subprocess.run([sys.executable, os.path.join("pipeline", "pipeline.py")])

if __name__ == "__main__":
    path = "app"
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Monitoring started... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
