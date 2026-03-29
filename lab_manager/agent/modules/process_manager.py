import psutil
import os

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes

def kill_process(pid: int):
    try:
        p = psutil.Process(pid)
        p.terminate()
        return True
    except psutil.NoSuchProcess:
        return False
