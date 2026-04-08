from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
import asyncio
from shared import constants, schemas
from ..api_client import APIClient

class CommandThread(QThread):
    """Поток для выполнения команд асинхронно"""
    finished = pyqtSignal(str)
    
    def __init__(self, api_client, ip, command):
        super().__init__()
        self.api_client = api_client
        self.ip = ip
        self.command = command
    
    def run(self):
        try:
            cmd = schemas.CommandRequest(command=self.command)
            result = asyncio.run(self.api_client.send_command(self.ip, cmd))
            self.finished.emit(f"✅ {self.command}: {result.get('status', 'ok')}")
        except Exception as e:
            self.finished.emit(f"❌ Ошибка: {str(e)}")

class ControlPanel(QWidget):
    """Панель управления рабочими станциями"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_client = APIClient("http://localhost:8000")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("🎮 Управление рабочими станциями")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Выбор станции
        station_layout = QHBoxLayout()
        station_layout.addWidget(QLabel("Выбрать ПК:"))
        self.station_combo = QComboBox()
        self.station_combo.addItems(["Все ПК", "ПК1", "ПК2", "ПК3"])
        station_layout.addWidget(self.station_combo)
        station_layout.addStretch()
        layout.addLayout(station_layout)
        
        # Группа команд: Система
        layout.addWidget(QLabel("📋 Системные команды:"))
        system_layout = QHBoxLayout()
        
        lock_btn = QPushButton("🔒 Заблокировать экран")
        lock_btn.clicked.connect(lambda: self.send_command("lock_screen"))
        system_layout.addWidget(lock_btn)
        
        shutdown_btn = QPushButton("🛑 Выключить ПК")
        shutdown_btn.setStyleSheet("background-color: #ff6b6b;")
        shutdown_btn.clicked.connect(lambda: self.send_command("shutdown"))
        system_layout.addWidget(shutdown_btn)
        
        restart_btn = QPushButton("🔄 Перезагрузить")
        restart_btn.clicked.connect(lambda: self.send_command("restart"))
        system_layout.addWidget(restart_btn)
        
        layout.addLayout(system_layout)
        
        # Группа команд: Сеть
        layout.addWidget(QLabel("🌐 Управление сетью:"))
        network_layout = QHBoxLayout()
        
        block_net_btn = QPushButton("🚫 Блокировать интернет")
        block_net_btn.clicked.connect(lambda: self.send_command("block_internet"))
        network_layout.addWidget(block_net_btn)
        
        unblock_net_btn = QPushButton("✅ Разблокировать интернет")
        unblock_net_btn.clicked.connect(lambda: self.send_command("unblock_internet"))
        network_layout.addWidget(unblock_net_btn)
        
        layout.addLayout(network_layout)
        
        # Группа команд: Процессы
        layout.addWidget(QLabel("⚙️ Управление процессами:"))
        process_layout = QHBoxLayout()
        
        kill_btn = QPushButton("✂️ Завершить процесс")
        kill_btn.clicked.connect(self.kill_process)
        process_layout.addWidget(kill_btn)
        
        layout.addLayout(process_layout)
        
        # Статус
        self.status_label = QLabel("Готово")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def send_command(self, command):
        """Отправить команду на ПК"""
        selected = self.station_combo.currentText()
        
        if selected == "Все ПК":
            ips = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]
        else:
            ips = ["192.168.1.10"]  # Пример IP
        
        for ip in ips:
            thread = CommandThread(self.api_client, ip, command)
            thread.finished.connect(self.on_command_finished)
            thread.start()
    
    def kill_process(self):
        """Завершить процесс"""
        pid, ok = self.get_pid_input()
        if ok and pid:
            self.send_command_with_params("kill_process", {"pid": pid})
    
    def send_command_with_params(self, command, params):
        """Отправить команду с параметрами"""
        try:
            selected = self.station_combo.currentText()
            ip = "192.168.1.10"  # Пример
            
            cmd = schemas.CommandRequest(command=command, params=params)
            asyncio.run(self.api_client.send_command(ip, cmd))
            self.status_label.setText(f"✅ Команда {command} выполнена")
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка: {str(e)}")
    
    def on_command_finished(self, message):
        """Обработать результат команды"""
        self.status_label.setText(message)
    
    def get_pid_input(self):
        """Получить PID процесса"""
        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(999999)
        dialog = QMessageBox()
        dialog.setWindowTitle("Завершить процесс")
        dialog.setText("Введите PID процесса:")
        # Упрощенный вариант - просто возвращаем значение
        return 1234, True

