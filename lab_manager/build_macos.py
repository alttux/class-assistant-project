#!/usr/bin/env python3
"""
Скрипт сборки Classroom Manager для macOS
Запускать на macOS системе с установленным PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def build_macos():
    """Сборка для macOS"""

    print("🚀 Начинаем сборку Classroom Manager для macOS...")

    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller найден")
    except ImportError:
        print("❌ PyInstaller не установлен. Установите: pip install pyinstaller")
        return False

    # Папка проекта
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist_macos"

    # Создаем папку для сборок
    dist_dir.mkdir(exist_ok=True)

    # Сборка GUI учителя
    print("\n📦 Сборка GUI учителя...")
    cmd_teacher = [
        "pyinstaller",
        "--onefile",  # Один исполняемый файл
        "--windowed",  # Без консоли (GUI приложение)
        "--name=ClassroomManager-Teacher",
        "--distpath", str(dist_dir),
        "--workpath", str(project_dir / "build_macos"),
        "--specpath", str(project_dir / "build_macos"),
        "--add-data", f"{project_dir}/server:server",
        "--add-data", f"{project_dir}/agent:agent",
        "--add-data", f"{project_dir}/shared:shared",
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
        "--name=ClassroomManager-Agent",
        "--distpath", str(dist_dir),
        "--workpath", str(project_dir / "build_macos"),
        "--specpath", str(project_dir / "build_macos"),
        "--add-data", f"{project_dir}/agent:agent",
        "--add-data", f"{project_dir}/shared:shared",
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

    # Создаем DMG образ (простая версия - ZIP)
    print("\n📦 Создание ZIP архива...")
    import zipfile

    zip_path = project_dir / "ClassroomManager_macOS.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arcname)

    print(f"✅ ZIP архив создан: {zip_path}")

    # Создаем README для macOS
    readme_content = """# Classroom Manager - macOS версия

## Установка
1. Распакуйте архив ClassroomManager_macOS.zip
2. Сделайте исполняемые: chmod +x ClassroomManager-Teacher ClassroomManager-Agent
3. Запустите ClassroomManager-Teacher (для учителя)
4. Или ClassroomManager-Agent (для ученика)

## Системные требования
- macOS 10.15+
- Нет необходимости в установке Python

## Использование
- Teacher: ./ClassroomManager-Teacher
- Agent: ./ClassroomManager-Agent

## Порты
- Сервер: 8000
- Агент: 8001

## Безопасность
Убедитесь, что файрвол разрешает соединения на портах 8000 и 8001.

## Примечание
При первом запуске macOS может показать предупреждение о безопасности.
Щелкните правой кнопкой мыши и выберите "Открыть" для разрешения запуска.
"""

    readme_path = dist_dir / "README_macOS.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ README создан: {readme_path}")

    print("🎉 Сборка для macOS завершена успешно!")
    print(f"📁 Файлы находятся в: {dist_dir}")
    print(f"📦 ZIP архив: {zip_path}")

    return True

if __name__ == "__main__":
    success = build_macos()
    if not success:
        sys.exit(1)
