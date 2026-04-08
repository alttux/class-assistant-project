from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel
from PyQt6.QtCore import Qt
import requests
from shared import constants

class MonitorPanel(QWidget):
    """Панель мониторинга системных ресурсов"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("📊 Мониторинг ресурсов")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Список рабочих станций с мониторингом
        self.stations_list = QListWidget()
        layout.addWidget(self.stations_list)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.refresh_monitor)
        button_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("🗑️ Очистить")
        clear_btn.clicked.connect(self.stations_list.clear)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def refresh_monitor(self):
        """Обновить данные мониторинга"""
        try:
            # Получить рабочие станции
            response = requests.get(f"http://localhost:{constants.DEFAULT_PORT}/workstations/")
            workstations = response.json()
            
            self.stations_list.clear()
            
            for ws in workstations:
                item_text = f"🖥️  {ws['name']} ({ws['ip_address']}) - {ws['status'].upper()}"
                item = QListWidgetItem(item_text)
                
                # Цвет статуса
                if ws['status'] == 'online':
                    item.setForeground(Qt.GlobalColor.green)
                else:
                    item.setForeground(Qt.GlobalColor.red)
                
                self.stations_list.addItem(item)
                
        except Exception as e:
            error_item = QListWidgetItem(f"❌ Ошибка: {str(e)}")
            self.stations_list.addItem(error_item)

