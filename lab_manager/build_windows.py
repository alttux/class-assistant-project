#!/usr/bin/env python3
"""
Скрипт сборки Classroom Manager для Windows
Запускать на Windows системе с установленным PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def build_windows():
    """Сборка для Windows"""

    print("🚀 Начинаем сборку Classroom Manager для Windows...")

    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller найден")
    except ImportError:
        print("❌ PyInstaller не установлен. Установите: pip install pyinstaller")
        return False

    # Папка проекта
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist_windows"

    # Создаем папку для сборок
    dist_dir.mkdir(exist_ok=True)

    # Сборка GUI учителя
    print("\n📦 Сборка GUI учителя...")
    cmd_teacher = [
        "pyinstaller",
        "--onefile",  # Один исполняемый файл
        "--windowed",  # Без консоли (GUI приложение)
        "--name=ClassroomManager_Teacher",
        "--distpath", str(dist_dir),
        "--workpath", str(project_dir / "build_windows"),
        "--specpath", str(project_dir / "build_windows"),
        "--add-data", f"{project_dir}/server;server",
        "--add-data", f"{project_dir}/agent;agent",
        "--add-data", f"{project_dir}/shared;shared",
        "--hidden-import", "psutil",
        "--hidden-import", "sqlalchemy",
        "--hidden-import", "fastapi",
        "--hidden-import", "uvicorn",
        "--hidden-import", "pydantic",
        "--hidden-import", "httpx",
        "--hidden-import", "reportlab",
        "run_teacher_gui.py"
    ]

    try:
        subprocess.run(cmd_teacher, check=True, cwd=project_dir)
        print("✅ GUI учителя собран успешно")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки GUI учителя: {e}")
        return False

    # Сборка GUI агента
    print("\n📦 Сборка GUI агента...")
    cmd_agent = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=ClassroomManager_Agent",
        "--distpath", str(dist_dir),
        "--workpath", str(project_dir / "build_windows"),
        "--specpath", str(project_dir / "build_windows"),
        "--add-data", f"{project_dir}/agent;agent",
        "--add-data", f"{project_dir}/shared;shared",
        "--hidden-import", "psutil",
        "--hidden-import", "fastapi",
        "--hidden-import", "uvicorn",
        "--hidden-import", "pydantic",
        "run_agent_gui.py"
    ]

    try:
        subprocess.run(cmd_agent, check=True, cwd=project_dir)
        print("✅ GUI агента собран успешно")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки GUI агента: {e}")
        return False

    # Создаем ZIP архив
    print("\n📦 Создание ZIP архива...")
    import zipfile

    zip_path = project_dir / "ClassroomManager_Windows.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arcname)

    print(f"✅ ZIP архив создан: {zip_path}")

    # Создаем README для Windows
    readme_content = """# Classroom Manager - Windows версия

## Установка
1. Распакуйте архив ClassroomManager_Windows.zip
2. Запустите ClassroomManager_Teacher.exe (для учителя)
3. Или ClassroomManager_Agent.exe (для ученика)

## Системные требования
- Windows 10/11
- Нет необходимости в установке Python

## Использование
- Teacher: Запустите ClassroomManager_Teacher.exe
- Agent: Запустите ClassroomManager_Agent.exe на каждом ПК ученика

## Порты
- Сервер: 8000
- Агент: 8001

## Безопасность
Убедитесь, что файрвол разрешает соединения на портах 8000 и 8001.
"""

    readme_path = dist_dir / "README_Windows.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ README создан: {readme_path}")

    print("🎉 Сборка для Windows завершена успешно!")
    print(f"📁 Файлы находятся в: {dist_dir}")
    print(f"📦 ZIP архив: {zip_path}")

    return True

if __name__ == "__main__":
    success = build_windows()
    if not success:
        sys.exit(1)
