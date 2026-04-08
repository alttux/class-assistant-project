from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
import requests
from shared import constants

class ReportsPanel(QWidget):
    """Панель отчетов и логирования"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("📄 Отчеты и логирование")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Список логов
        layout.addWidget(QLabel("История событий:"))
        self.logs_list = QListWidget()
        layout.addWidget(self.logs_list)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Обновить логи")
        refresh_btn.clicked.connect(self.refresh_logs)
        button_layout.addWidget(refresh_btn)
        
        report_btn = QPushButton("📊 Сгенерировать отчет")
        report_btn.setStyleSheet("background-color: #4dabf7;")
        report_btn.clicked.connect(self.generate_report)
        button_layout.addWidget(report_btn)
        
        export_btn = QPushButton("💾 Экспортировать в PDF")
        export_btn.setStyleSheet("background-color: #ffa94d;")
        export_btn.clicked.connect(self.export_pdf)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        # Статус
        self.status_label = QLabel("Готово")
        self.status_label.setStyleSheet("color: green;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Загрузить логи
        self.refresh_logs()
    
    def refresh_logs(self):
        """Загрузить логи с сервера"""
        try:
            response = requests.get(f"http://localhost:{constants.DEFAULT_PORT}/logs/")
            logs = response.json()
            
            self.logs_list.clear()
            
            for log in reversed(logs):  # Новые сверху
                timestamp = log.get('timestamp', 'N/A')[:16]
                action = log.get('action', 'Unknown')
                details = log.get('details', '')
                
                item_text = f"[{timestamp}] {action} - {details}"
                item = QListWidgetItem(item_text)
                item.setForeground(Qt.GlobalColor.darkGray)
                self.logs_list.addItem(item)
            
            self.status_label.setText(f"✅ Загружено {len(logs)} событий")
            
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка: {str(e)}")
    
    def generate_report(self):
        """Сгенерировать отчет"""
        try:
            response = requests.get(f"http://localhost:{constants.DEFAULT_PORT}/report")
            report = response.json()
            
            self.logs_list.clear()
            
            # Показать информацию отчета
            items = [
                f"📊 Отчет по использованию",
                f"Период: {report.get('period', 'N/A')}",
                f"Всего действий: {report.get('total_actions', 0)}",
                f"Действия: {', '.join(report.get('actions', []))}",
            ]
            
            for item_text in items:
                item = QListWidgetItem(item_text)
                item.setForeground(Qt.GlobalColor.darkBlue)
                self.logs_list.addItem(item)
            
            self.status_label.setText("✅ Отчет сгенерирован")
            
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка: {str(e)}")
    
    def export_pdf(self):
        """Экспортировать отчет в PDF"""
        try:
            response = requests.post(f"http://localhost:{constants.DEFAULT_PORT}/export_report")
            result = response.json()
            self.status_label.setText(f"✅ Отчет экспортирован: {result.get('status', 'ok')}")
            
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка: {str(e)}")

