from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QComboBox
from PyQt6.QtCore import Qt
import requests
from shared import constants

class ProfilePanel(QWidget):
    """Панель управления профилями"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("👤 Управление профилями")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Список профилей
        layout.addWidget(QLabel("Доступные профили:"))
        self.profiles_list = QListWidget()
        layout.addWidget(self.profiles_list)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.clicked.connect(self.refresh_profiles)
        button_layout.addWidget(refresh_btn)
        
        apply_btn = QPushButton("✅ Применить профиль")
        apply_btn.setStyleSheet("background-color: #51cf66;")
        apply_btn.clicked.connect(self.apply_profile)
        button_layout.addWidget(apply_btn)
        
        new_btn = QPushButton("➕ Создать профиль")
        new_btn.clicked.connect(self.create_profile)
        button_layout.addWidget(new_btn)
        
        layout.addLayout(button_layout)
        
        # Статус
        self.status_label = QLabel("Готово")
        self.status_label.setStyleSheet("color: green;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Загрузить профили при инициализации
        self.refresh_profiles()
    
    def refresh_profiles(self):
        """Загрузить профили с сервера"""
        try:
            response = requests.get(f"http://localhost:{constants.DEFAULT_PORT}/profiles/")
            profiles = response.json()
            
            self.profiles_list.clear()
            
            for profile in profiles:
                item_text = f"📋 {profile['name']} - {profile.get('description', 'Нет описания')}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, profile['id'])
                self.profiles_list.addItem(item)
            
            self.status_label.setText(f"✅ Загружено {len(profiles)} профилей")
            
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка: {str(e)}")
    
    def apply_profile(self):
        """Применить выбранный профиль"""
        current = self.profiles_list.currentItem()
        if not current:
            self.status_label.setText("❌ Выберите профиль")
            return
        
        profile_name = current.text().split(" - ")[0].replace("📋 ", "")
        
        try:
            # Применить профиль ко всем ПК
            data = {
                "profile_name": profile_name,
                "workstations": ["192.168.1.10", "192.168.1.11"]
            }
            response = requests.post(
                f"http://localhost:{constants.DEFAULT_PORT}/apply_profile",
                json=data
            )
            self.status_label.setText(f"✅ Профиль '{profile_name}' применен")
            
        except Exception as e:
            self.status_label.setText(f"❌ Ошибка: {str(e)}")
    
    def create_profile(self):
        """Создать новый профиль"""
        # Упрощенная версия
        self.status_label.setText("➕ Новый профиль (требуется расширенный интерфейс)")

