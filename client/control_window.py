'''
Robot Control Window
'''

import sys
from gui.controllers.control_controller import ControlController
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QMainWindow,
    QPlainTextEdit,
    QLineEdit,
    QLabel
)
from PyQt6.QtGui import QPixmap
import threading
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import subprocess
# Get external IP address using a third-party service (e.g., ifconfig.me)
external_ip = requests.get('https://ifconfig.me/ip').text.strip()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

class ControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Training")
        self.setFixedSize(300,200)
        self.generalLayout  = QGridLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createWidgets()
    def _createWidgets(self):
        self.widget_map = {}
        self.widget_map["start_client"] = QPushButton("Start client trainer")
        self.widget_map['image_label'] = QLabel(self)
        self.widget_map['pixmap'] = QPixmap('frontend/gui/test.png')
        if self.widget_map['pixmap'].isNull():
            print("Error loading image")
            print(os.getcwd())
                # set size of image
        else:
            self.widget_map['image_label'].setFixedWidth(500)
        self.widget_map['image_label'].setPixmap(self.widget_map['pixmap'])
        self.generalLayout.addWidget(self.widget_map["start_client"], 0, 0)
        self.generalLayout.addWidget(self.widget_map['image_label'], 0, 1)

qApp = QApplication(sys.argv)
view = ControlWindow()
def run_server():
    uvicorn.run(app, host=external_ip, port=8002)


@app.post("/start_client")
async def start():
    print("Starting client")
    subprocess.Popen(["uvicorn", "client:app", "--host", external_ip, "--port", "8001"])
    return {"message": "Client started"}
   


@app.post("/image")
async def image(data):
    print("image received")


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    controller = ControlController(view=view)
    view.show()

    sys.exit(qApp.exec())