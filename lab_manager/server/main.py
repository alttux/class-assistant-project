import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QListWidget, QHBoxLayout
from PyQt6.QtCore import QThread
import uvicorn
from .api import app as fastapi_app
from .api_client import APIClient
from shared import constants, schemas

class ServerThread(QThread):
    def run(self):
        uvicorn.run(fastapi_app, host=constants.SERVER_HOST, port=constants.DEFAULT_PORT)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Classroom Manager")
        self.setGeometry(100, 100, 800, 600)

        self.api_client = APIClient(f"http://{constants.SERVER_IP}:{constants.DEFAULT_PORT}")

        layout = QVBoxLayout()

        self.label = QLabel("Server running on port 8000")
        layout.addWidget(self.label)

        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)
        layout.addWidget(self.start_button)

        # Workstation list
        self.workstation_list = QListWidget()
        layout.addWidget(self.workstation_list)

        # Control buttons
        button_layout = QHBoxLayout()
        self.lock_button = QPushButton("Lock All Screens")
        self.lock_button.clicked.connect(self.lock_screens)
        button_layout.addWidget(self.lock_button)

        self.shutdown_button = QPushButton("Shutdown All")
        self.shutdown_button.clicked.connect(self.shutdown_all)
        button_layout.addWidget(self.shutdown_button)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.server_thread = None

    def start_server(self):
        if not self.server_thread:
            self.server_thread = ServerThread()
            self.server_thread.start()
            self.label.setText("Server started")

    def lock_screens(self):
        # For demo, assume workstations
        workstations = ["192.168.1.10", "192.168.1.11"]  # Hardcoded
        for ip in workstations:
            asyncio.run(self.send_command(ip, "lock_screen"))

    def shutdown_all(self):
        workstations = ["192.168.1.10", "192.168.1.11"]
        for ip in workstations:
            asyncio.run(self.send_command(ip, "shutdown"))

    async def send_command(self, ip, command):
        cmd = schemas.CommandRequest(command=command)
        await self.api_client.send_command(ip, cmd)

if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec())
