import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStatusBar, QMenuBar, QMenu)
from PyQt6.QtCore import QThread, QTimer, Qt
from PyQt6.QtGui import QIcon, QFont, QColor
from PyQt6.QtCore import pyqtSignal
import uvicorn
import threading

from .monitor_panel import MonitorPanel
from .control_panel import ControlPanel
from .profile_panel import ProfilePanel
from .reports_panel import ReportsPanel
from ..api import app
from shared import constants

class ServerThread(QThread):
    """Фоновый поток для запуска FastAPI сервера"""
    started = pyqtSignal(str)
    
    def run(self):
        try:
            self.started.emit("🟢 Сервер запущен")
            uvicorn.run(app, host="0.0.0.0", port=constants.DEFAULT_PORT, log_level="info")
        except Exception as e:
            self.started.emit(f"🔴 Ошибка сервера: {str(e)}")

class TeacherMainWindow(QMainWindow):
    """Главное окно учителя для управления классом"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 Classroom Manager - Панель управления учителя")
        self.setGeometry(100, 100, 1200, 700)
        
        # Переменные
        self.server_thread = None
        self.server_running = False
        
        # UI
        self.init_ui()
        self.create_menu()
        
        # Статус
        self.statusBar().showMessage("Инициализация...")
        
        # Таймер для обновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.periodic_refresh)
        
    def init_ui(self):
        """Инициализировать пользовательский интерфейс"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Панель управления сервером
        server_layout = QHBoxLayout()
        server_label = QLabel("🖥️ Состояние сервера:")
        server_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        server_layout.addWidget(server_label)
        
        self.server_status = QLabel("🔴 Остановлен")
        self.server_status.setStyleSheet("color: red; font-weight: bold;")
        server_layout.addWidget(self.server_status)
        
        start_server_btn = QPushButton("▶️ Запустить сервер")
        start_server_btn.setStyleSheet("background-color: #51cf66; color: white; font-weight: bold;")
        start_server_btn.clicked.connect(self.start_server)
        server_layout.addWidget(start_server_btn)
        
        stop_server_btn = QPushButton("⏹️ Остановить сервер")
        stop_server_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
        stop_server_btn.clicked.connect(self.stop_server)
        server_layout.addWidget(stop_server_btn)
        
        server_layout.addStretch()
        main_layout.addLayout(server_layout)
        
        # Разделитель
        separator = QLabel("─" * 80)
        main_layout.addWidget(separator)
        
        # Вкладки для разных функций
        self.tabs = QTabWidget()
        
        # Вкладка 1: Мониторинг
        self.monitor_panel = MonitorPanel()
        self.tabs.addTab(self.monitor_panel, "📊 Мониторинг")
        
        # Вкладка 2: Управление
        self.control_panel = ControlPanel()
        self.tabs.addTab(self.control_panel, "🎮 Управление")
        
        # Вкладка 3: Профили
        self.profile_panel = ProfilePanel()
        self.tabs.addTab(self.profile_panel, "👤 Профили")
        
        # Вкладка 4: Отчеты
        self.reports_panel = ReportsPanel()
        self.tabs.addTab(self.reports_panel, "📄 Отчеты")
        
        main_layout.addWidget(self.tabs)
        
        # Нижняя панель
        footer_layout = QHBoxLayout()
        footer_layout.addWidget(QLabel("💡 Совет: Регулярно обновляйте данные мониторинга"))
        footer_layout.addStretch()
        version_label = QLabel("v1.0.0 | Ready for Classroom")
        version_label.setStyleSheet("color: gray;")
        footer_layout.addWidget(version_label)
        main_layout.addLayout(footer_layout)
        
        central_widget.setLayout(main_layout)
    
    def create_menu(self):
        """Создать меню приложения"""
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu("📁 Файл")
        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)
        
        # Меню "Управление"
        manage_menu = menubar.addMenu("⚙️ Управление")
        refresh_action = manage_menu.addAction("🔄 Обновить все")
        refresh_action.triggered.connect(self.refresh_all)
        
        manage_menu.addSeparator()
        discovery_action = manage_menu.addAction("🔍 Поиск агентов")
        discovery_action.triggered.connect(self.discover_agents)
        
        # Меню "Справка"
        help_menu = menubar.addMenu("❓ Справка")
        about_action = help_menu.addAction("О приложении")
        about_action.triggered.connect(self.show_about)
    
    def start_server(self):
        """Запустить FastAPI сервер"""
        if not self.server_running:
            self.server_thread = ServerThread()
            self.server_thread.started.connect(self.on_server_status)
            self.server_thread.start()
            self.server_running = True
            
            # Запустить таймер обновления
            self.timer.start(5000)  # Обновлять каждые 5 секунд
            
            self.statusBar().showMessage("Сервер запущен на http://localhost:8000")
    
    def stop_server(self):
        """Остановить сервер"""
        if self.server_running:
            self.timer.stop()
            self.server_thread.quit()
            self.server_thread.wait()
            self.server_running = False
            
            self.server_status.setText("🔴 Остановлен")
            self.server_status.setStyleSheet("color: red; font-weight: bold;")
            self.statusBar().showMessage("Сервер остановлен")
    
    def on_server_status(self, message):
        """Обновить статус сервера"""
        if "запущен" in message.lower():
            self.server_status.setText("🟢 Работает")
            self.server_status.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.server_status.setText("🔴 Ошибка")
            self.server_status.setStyleSheet("color: red; font-weight: bold;")
        
        self.statusBar().showMessage(message)
    
    def periodic_refresh(self):
        """Периодическое обновление данных"""
        self.monitor_panel.refresh_monitor()
    
    def refresh_all(self):
        """Обновить все панели"""
        self.monitor_panel.refresh_monitor()
        self.profile_panel.refresh_profiles()
        self.reports_panel.refresh_logs()
        self.statusBar().showMessage("✅ Все данные обновлены")
    
    def discover_agents(self):
        """Найти активные агенты в сети"""
        self.statusBar().showMessage("🔍 Поиск агентов в сети...")
        # Реализация в следующей версии
        self.statusBar().showMessage("Поиск: функция в разработке")
    
    def show_about(self):
        """Показать информацию о приложении"""
        about_text = """
        🎓 Classroom Manager v1.0.0
        
        Система управления IT классом
        
        Функции:
        • Управление рабочими станциями
        • Мониторинг в реальном времени
        • Управление профилями
        • Отчеты и логирование
        
        Разработано для образовательных учреждений
        """
        self.statusBar().showMessage(about_text)
    
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        if self.server_running:
            self.stop_server()
        event.accept()

def run_gui():
    """Запустить GUI приложение"""
    app = QApplication(sys.argv)
    
    # Установить стиль
    app.setStyle('Fusion')
    
    # Создать главное окно
    window = TeacherMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()

