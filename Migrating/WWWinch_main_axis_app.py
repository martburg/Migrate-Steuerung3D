import sys
import os
import signal
import time
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

achse_proc = None  # For use in signal handler


def shutdown_backend():
    global achse_proc
    if achse_proc and achse_proc.poll() is None:
        print("[Main] Terminating backend process...")
        achse_proc.terminate()
        try:
            achse_proc.wait(timeout=2)
        except Exception:
            achse_proc.kill()
        print("[Main] Backend shutdown complete.")


def signal_handler(signum, frame):
    print(f"[Main] Received signal: {signum}")
    shutdown_backend()
    sys.exit(0)


def main():
    global achse_proc

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    app = QApplication(sys.argv)

    controler = None

    # --- Launch UI ---
    try:
        time.sleep(0.2)  # Let backend init shared memory

        widget = Widget()

        controller = Controller(widget)

        controller.start()

        widget.show()
        exit_code = app.exec()

    finally:
        shutdown_backend()
        if controller is not None:
            controller.shutdown()  # ← this ensures shm is cleaned

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
