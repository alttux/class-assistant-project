from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import requests
from shared import constants
from ..api_client import APIClient

class CommandThread(QThread):
    """Поток для выполнения команд асинхронно"""
    finished = pyqtSignal(str)
    
    def __init__(self, ip, command, params=None):
        super().__init__()
        self.ip = ip
        self.command = command
        self.params = params

    def run(self):
        try:
            url = f"http://{self.ip}:{constants.DEFAULT_PORT}/command/{self.ip}"
            headers = {"Authorization": f"Bearer {constants.AUTH_TOKEN}"}
            data = {"command": self.command}
            if self.params:
                data["params"] = self.params
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                self.finished.emit(f"✅ {self.command}: {result.get('status', 'ok')}")
            else:
                self.finished.emit(f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.finished.emit(f"❌ Ошибка: {str(e)}")

class ControlPanel(QWidget):
    """Панель управления рабочими станциями"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.api_client = APIClient(f"http://{constants.SERVER_IP}:{constants.DEFAULT_PORT}")
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
        
        # Хранилище IP адресов
        self.workstations_ips = {
            "ПК1": "192.168.1.10",
            "ПК2": "192.168.1.11",
            "ПК3": "192.168.1.12"
        }

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
            ips = list(self.workstations_ips.values())
        else:
            ips = [self.workstations_ips.get(selected, "192.168.1.10")]

        for ip in ips:
            thread = CommandThread(ip, command)
            thread.finished.connect(self.on_command_finished)
            thread.start()
    
    def kill_process(self):
        """Завершить процесс"""
        pid, ok = self.get_pid_input()
        if ok and pid:
            self.send_command_with_params("kill_process", {"pid": pid})
    
    def send_command_with_params(self, command, params):
        """Отправить команду с параметрами"""
        selected = self.station_combo.currentText()
        ip = "192.168.1.10"  # Пример

        thread = CommandThread(ip, command, params)
        thread.finished.connect(self.on_command_finished)
        thread.start()

    def on_command_finished(self, message):
        """Обработать результат команды"""
        self.status_label.setText(message)
    
    def update_workstations(self, agent_ips: list):
        """Обновить список рабочих станций на основе найденных агентов"""
        self.workstations_ips.clear()
        for idx, ip in enumerate(agent_ips, 1):
            pc_name = f"ПК{idx}"
            self.workstations_ips[pc_name] = ip

        # Обновить комбобокс
        current_items = [self.station_combo.itemText(i) for i in range(self.station_combo.count())]
        pc_items = list(self.workstations_ips.keys())

        if set(current_items[1:]) != set(pc_items):  # Пропускаем "Все ПК"
            self.station_combo.clear()
            self.station_combo.addItem("Все ПК")
            for pc_name in pc_items:
                self.station_combo.addItem(pc_name)

            self.status_label.setText(f"✅ Обновлено. Найдено {len(agent_ips)} ПК")

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
