import sys
import subprocess
import time
from app.core.config import settings

def run_production():
    subprocess.run([
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", settings.HOST,
        "--port", str(settings.PORT),
        "--log-level", "info"
    ])

def run_development():
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class RestartHandler(FileSystemEventHandler):
        def __init__(self):
            self.process = None
            self.start_server()

        def start_server(self):
            if self.process:
                self.process.terminate()
                self.process.wait()
            self.process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "app.main:app",
                "--host", settings.HOST,
                "--port", str(settings.PORT),
                "--log-level", "debug"
            ])

        def on_modified(self, event):
            if event.src_path.endswith(".py"):
                print(f"\nCambio detectado: {event.src_path}, reiniciando...")
                self.start_server()

    handler = RestartHandler()
    observer = Observer()
    observer.schedule(handler, path="app/", recursive=True)
    observer.start()
    print("Watching for changes in app/...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        handler.process.terminate()
    observer.join()

if __name__ == "__main__":
    if settings.DEBUG:
        run_development()
    else:
        run_production()