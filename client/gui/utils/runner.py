from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from typing import Callable
import subprocess

class CommandRunner(QThread):
    output_signal = pyqtSignal(str)
    def __init__(self, env: dict):
        super().__init__()
        self.env = env
    def run(self):
        print("Running command", self.command)
        self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, \
            stderr=subprocess.STDOUT,stdin=subprocess.PIPE, shell=True, env=self.env)
        while True:
            output = self.process.stdout.readline()
            if output:
                self.output_signal.emit(output.strip().decode('utf-8'))
            elif self.process.poll() is not None:
                print("process finished")
                break
        rc = self.process.poll()
        #return rc
    def set_command(self, command: str):
        self.command = command
    def send_input(self, input_text: str):
        self.process.stdin.write(input_text.encode())
        self.process.stdin.flush()
