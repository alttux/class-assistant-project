#!/usr/bin/env python3
"""
Запуск GUI учителя (Classroom Manager)

Использование:
    python run_teacher_gui.py
"""

import sys
import os

# Добавить путь к проекту
sys.path.insert(0, os.path.dirname(__file__))

from server.gui.main_window import run_gui

if __name__ == "__main__":
    print("🎓 Запуск Classroom Manager - Панель управления учителя...")
    print("📡 Интерфейс будет доступен на http://localhost:8000")
    run_gui()

