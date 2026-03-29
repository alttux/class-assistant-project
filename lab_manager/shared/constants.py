# Constants for the application

DEFAULT_PORT = 8000
AGENT_PORT = 8001
TIMEOUT = 10  # seconds
AUTH_TOKEN = "secret_token"  # For simplicity, in production use proper auth

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
