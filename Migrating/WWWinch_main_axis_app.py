import sys
import os
import signal
import time
import atexit
from subprocess import Popen, CalledProcessError, SubprocessError
from PySide6.QtWidgets import QApplication, QMessageBox
from WWWinch_widget import Widget
from WWWinch_controler import Controller

ACHSEN = {
    'Anton':  ("172.16.17.1", 15001, "172.16.17.5", 15001),
    'Burt':   ("172.16.17.2", 15001, "172.16.17.5", 15002),
    'Cecil':  ("172.16.17.3", 15001, "172.16.17.5", 15003),
    'Debby':  ("172.16.17.4", 15001, "172.16.17.5", 15004),
    'Eugene': ("172.16.17.5", 15001, "172.16.17.5", 15005),
    'Fred':   ("172.16.17.6", 15001, "172.16.17.5", 15006),
    'SIMUL':  ("127.0.0.1", 15001, "127.0.0.1", 15005),
}

controller = None  # Global so signal and atexit handlers can access it


def safe_shutdown():
    global controller
    if controller is not None:
        print("[Main] Triggering safe shutdown...")
        controller.stop_backend()
        controller.shutdown()
        controller = None  # Prevent double shutdown


def handle_signal(signum, frame):
    print(f"[Main] Caught signal {signum}, shutting down...")
    safe_shutdown()
    sys.exit(0)


def main():
    global controller

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    atexit.register(safe_shutdown)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(safe_shutdown)

    try:
        time.sleep(0.2)  # Let backend init shared memory

        widget = Widget()
        controller = Controller(widget)
        widget.controller = controller

        controller.start()
        widget.show()

        exit_code = app.exec()

    finally:
        safe_shutdown()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
