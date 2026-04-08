#!/usr/bin/env python3
"""
Запуск GUI агента (Student Agent)

Использование:
    python run_agent_gui.py
"""

import sys
import os

# Добавить путь к проекту
sys.path.insert(0, os.path.dirname(__file__))

from agent.gui import run_agent_gui

if __name__ == "__main__":
    print("📚 Запуск Student PC Agent...")
    print("📡 Агент будет доступен на http://localhost:8001")
    run_agent_gui()

