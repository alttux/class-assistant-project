#!/usr/bin/env python3
"""
Скрипт сборки Classroom Manager для Linux
Запускать на Linux системе с установленным PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def build_linux():
    """Сборка для Linux"""

    print("🚀 Начинаем сборку Classroom Manager для Linux...")

    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller найден")
    except ImportError:
        print("❌ PyInstaller не установлен. Установите: pip install pyinstaller")
        return False

    # Папка проекта
    project_dir = Path(__file__).parent
    dist_dir = project_dir / "dist_linux"

    # Создаем папку для сборок
    dist_dir.mkdir(exist_ok=True)

    # Сборка GUI учителя
    print("\n📦 Сборка GUI учителя...")
    cmd_teacher = [
        "pyinstaller",
        "--onefile",  # Один исполняемый файл
        "--windowed",  # Без консоли (GUI приложение)
        "--name=classroom-manager-teacher",
        "--distpath", str(dist_dir),
        "--workpath", str(project_dir / "build_linux"),
        "--specpath", str(project_dir / "build_linux"),
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
        "--name=classroom-manager-agent",
        "--distpath", str(dist_dir),
        "--workpath", str(project_dir / "build_linux"),
        "--specpath", str(project_dir / "build_linux"),
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

    # Создаем TAR.GZ архив
    print("\n📦 Создание TAR.GZ архива...")
    import tarfile

    tar_path = project_dir / "ClassroomManager_Linux.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                tar.add(file_path, arcname=arcname)

    print(f"✅ TAR.GZ архив создан: {tar_path}")

    # Создаем README для Linux
    readme_content = """# Classroom Manager - Linux версия

## Установка
1. Распакуйте архив: tar -xzf ClassroomManager_Linux.tar.gz
2. Сделайте исполняемые: chmod +x classroom-manager-teacher classroom-manager-agent
3. Запустите classroom-manager-teacher (для учителя)
4. Или classroom-manager-agent (для ученика)

## Системные требования
- Linux (Ubuntu, CentOS, Fedora, etc.)
- GTK+ libraries для PyQt6
- Нет необходимости в установке Python

## Использование
- Teacher: ./classroom-manager-teacher
- Agent: ./classroom-manager-agent

## Порты
- Сервер: 8000
- Агент: 8001

## Зависимости системы
Убедитесь, что установлены:
- libxcb-xinerama0
- libxcb-icccm4
- libxcb-image0
- libxcb-keysyms1
- libxcb-randr0
- libxcb-render-util0
- libxcb-shape0

## Безопасность
Убедитесь, что файрвол разрешает соединения на портах 8000 и 8001.
"""

    readme_path = dist_dir / "README_Linux.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ README создан: {readme_path}")

    print("🎉 Сборка для Linux завершена успешно!")
    print(f"📁 Файлы находятся в: {dist_dir}")
    print(f"📦 TAR.GZ архив: {tar_path}")

    return True

if __name__ == "__main__":
    success = build_linux()
    if not success:
        sys.exit(1)
