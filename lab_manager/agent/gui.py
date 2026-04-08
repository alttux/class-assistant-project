import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QProgressBar, QPushButton, QTextEdit)
from PyQt6.QtCore import QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import psutil
import platform

class SystemMonitorThread(QThread):
    """Поток для мониторинга системы"""
    cpu_updated = pyqtSignal(float)
    ram_updated = pyqtSignal(float)
    disk_updated = pyqtSignal(float)
    
    def run(self):
        while True:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                
                self.cpu_updated.emit(cpu)
                self.ram_updated.emit(ram)
                self.disk_updated.emit(disk)
                
                self.msleep(2000)  # Обновлять каждые 2 секунды
            except Exception as e:
                print(f"Ошибка мониторинга: {e}")
                self.msleep(2000)

class StudentAgentUI(QMainWindow):
    """GUI для ученика (агента на ПК ученика)"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"📚 Student PC Agent - {platform.node()}")
        self.setGeometry(100, 100, 600, 500)
        
        # Переменные состояния
        self.is_locked = False
        self.agent_running = True
        
        self.init_ui()
        
        # Запустить мониторинг
        self.monitor_thread = SystemMonitorThread()
        self.monitor_thread.cpu_updated.connect(self.update_cpu)
        self.monitor_thread.ram_updated.connect(self.update_ram)
        self.monitor_thread.disk_updated.connect(self.update_disk)
        self.monitor_thread.start()
    
    def init_ui(self):
        """Инициализировать интерфейс"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("🖥️ Student Agent Panel")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Информация о ПК
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel(f"ОС: {platform.system()} {platform.release()}"))
        info_layout.addWidget(QLabel(f"Процессор: {platform.processor()}"))
        layout.addLayout(info_layout)
        
        # Разделитель
        layout.addWidget(QLabel("─" * 60))
        
        # Мониторинг ресурсов
        layout.addWidget(QLabel("📊 Мониторинг ресурсов:", font=QFont("Arial", 11, QFont.Weight.Bold)))
        
        # CPU
        cpu_label_layout = QHBoxLayout()
        cpu_label_layout.addWidget(QLabel("CPU:"))
        self.cpu_label = QLabel("0%")
        self.cpu_label.setStyleSheet("font-weight: bold; color: blue;")
        cpu_label_layout.addWidget(self.cpu_label)
        cpu_label_layout.addStretch()
        layout.addLayout(cpu_label_layout)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        layout.addWidget(self.cpu_bar)
        
        # RAM
        ram_label_layout = QHBoxLayout()
        ram_label_layout.addWidget(QLabel("RAM:"))
        self.ram_label = QLabel("0%")
        self.ram_label.setStyleSheet("font-weight: bold; color: blue;")
        ram_label_layout.addWidget(self.ram_label)
        ram_label_layout.addStretch()
        layout.addLayout(ram_label_layout)
        
        self.ram_bar = QProgressBar()
        self.ram_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
            }
        """)
        layout.addWidget(self.ram_bar)
        
        # DISK
        disk_label_layout = QHBoxLayout()
        disk_label_layout.addWidget(QLabel("DISK:"))
        self.disk_label = QLabel("0%")
        self.disk_label.setStyleSheet("font-weight: bold; color: blue;")
        disk_label_layout.addWidget(self.disk_label)
        disk_label_layout.addStretch()
        layout.addLayout(disk_label_layout)
        
        self.disk_bar = QProgressBar()
        self.disk_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #f39c12;
            }
        """)
        layout.addWidget(self.disk_bar)
        
        # Разделитель
        layout.addWidget(QLabel("─" * 60))
        
        # Журнал событий
        layout.addWidget(QLabel("📝 Журнал событий:", font=QFont("Arial", 11, QFont.Weight.Bold)))
        self.event_log = QTextEdit()
        self.event_log.setReadOnly(True)
        self.event_log.setMaximumHeight(150)
        layout.addWidget(self.event_log)
        
        # Кнопки управления (демонстрация)
        button_layout = QHBoxLayout()
        
        self.lock_btn = QPushButton("🔒 Заблокирован" if self.is_locked else "🔓 Разблокирован")
        self.lock_btn.setStyleSheet("background-color: #95a5a6;")
        self.lock_btn.setEnabled(False)  # Только для информации
        button_layout.addWidget(self.lock_btn)
        
        self.agent_status = QPushButton("🟢 Агент активен")
        self.agent_status.setStyleSheet("background-color: #27ae60;")
        self.agent_status.setEnabled(False)  # Только для информации
        button_layout.addWidget(self.agent_status)
        
        layout.addLayout(button_layout)
        
        # Статус
        self.status_label = QLabel("✅ Агент подключен и готов к командам")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        central_widget.setLayout(layout)
        
        # Логирование при запуске
        self.log_event("🟢 Агент запущен на http://localhost:8001")
        self.log_event(f"🖥️ Компьютер: {platform.node()}")
        self.log_event("⏳ Ожидание команд от учителя...")
    
    def update_cpu(self, value):
        """Обновить CPU метрику"""
        self.cpu_label.setText(f"{value:.1f}%")
        self.cpu_bar.setValue(int(value))
    
    def update_ram(self, value):
        """Обновить RAM метрику"""
        self.ram_label.setText(f"{value:.1f}%")
        self.ram_bar.setValue(int(value))
    
    def update_disk(self, value):
        """Обновить DISK метрику"""
        self.disk_label.setText(f"{value:.1f}%")
        self.disk_bar.setValue(int(value))
    
    def log_event(self, message):
        """Добавить событие в журнал"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.event_log.append(f"[{timestamp}] {message}")
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.monitor_thread.quit()
        self.monitor_thread.wait()
        event.accept()

def run_agent_gui():
    """Запустить GUI агента"""
    app = QApplication(sys.argv)
    
    # Установить стиль
    app.setStyle('Fusion')
    
    # Создать окно агента
    window = StudentAgentUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    run_agent_gui()

