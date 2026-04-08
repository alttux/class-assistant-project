# Constants for the application
import socket

def get_local_ip():
    """Получить локальный IP адрес в сети"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

DEFAULT_PORT = 8000
AGENT_PORT = 8001
TIMEOUT = 10  # seconds
AUTH_TOKEN = "secret_token"  # For simplicity, in production use proper auth

# Server configuration
SERVER_HOST = "0.0.0.0"  # Listen on all interfaces
SERVER_IP = get_local_ip()  # For client connections

# Command codes
COMMANDS = {
    "lock_screen": "lock_screen",
    "unlock_screen": "unlock_screen",
    "shutdown": "shutdown",
    "restart": "restart",
    "kill_process": "kill_process",
    "send_message": "send_message",
    "apply_profile": "apply_profile",
    "block_internet": "block_internet",
    "unblock_internet": "unblock_internet",
    "monitor": "monitor"
}
