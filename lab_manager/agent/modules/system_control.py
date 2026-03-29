import subprocess
import platform

def lock_screen():
    if platform.system() == "Windows":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-screensaver", "lock"])
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["pmset", "displaysleepnow"])

def shutdown():
    if platform.system() == "Windows":
        subprocess.run(["shutdown", "/s", "/t", "0"])
    else:
        subprocess.run(["shutdown", "now"])

def restart():
    if platform.system() == "Windows":
        subprocess.run(["shutdown", "/r", "/t", "0"])
    else:
        subprocess.run(["reboot"])
