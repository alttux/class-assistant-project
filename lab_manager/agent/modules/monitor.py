import psutil

def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return {
        "cpu_usage": cpu,
        "ram_usage": ram,
        "disk_usage": disk
    }

def get_processes():
    return [{"pid": p.info['pid'], "name": p.info['name']} for p in psutil.process_iter(['pid', 'name'])]
