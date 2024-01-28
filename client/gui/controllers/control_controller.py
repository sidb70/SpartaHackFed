#from utils.runner import CommandRunner
from PyQt6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QWidget,
    QLabel,
    QMainWindow,
)
from typing import Callable
from PyQt6.QtCore import Qt, QTimer
import os
import requests
# Get external IP address using a third-party service (e.g., ifconfig.me)
external_ip = requests.get('https://ifconfig.me/ip').text.strip()


class ControlController:
    def __init__(self, view: QMainWindow):
        self._view = view
        self.processes = {}
        self._connectSignalsAndSlots()
    def _connectSignalsAndSlots(self):
        self._view.widget_map["start_client"].clicked.connect(self.start_client)

    # --------------------Slots-------------------- #
    def start_client(self):
        requests.post("http://"+external_ip+":8002/start_client/")
        print("Starting client")
   