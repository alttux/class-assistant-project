#!/usr/bin/env python3
"""
Classroom Manager - Deploy Script
Помощь при развертывании системы в сети
"""

import os
import sys
import socket
import platform
from pathlib import Path

def get_local_ip():
    """Get machine's local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 60)
    print("  🎓 CLASSROOM MANAGER - DEPLOYMENT HELPER")
    print("=" * 60 + "\n")

def print_system_info():
    """Print system information"""
    print("📊 SYSTEM INFORMATION")
    print("-" * 60)
    print(f"  Operating System: {platform.system()} {platform.release()}")
    print(f"  Python Version: {platform.python_version()}")
    print(f"  Local IP: {get_local_ip()}")
    print(f"  Computer Name: {socket.gethostname()}")
    print("-" * 60 + "\n")

def print_server_instructions():
    """Print server deployment instructions"""
    print("🖥️  SERVER SETUP (Teacher's Machine)")
    print("-" * 60)
    print("""
1. Open Terminal/Command Prompt
2. Navigate to project: cd lab_manager
3. Install dependencies: pip install -r requirements.txt
4. Run server: python -m server.gui.main_window
5. Click "▶️ Запустить сервер" button
6. Go to "⚙️ Управление" → "🔍 Поиск агентов"
7. Wait for agents to be discovered

Server will be accessible at:
  - Local: http://localhost:8000
  - Network: http://{ip}:8000
""".format(ip=get_local_ip()))
    print("-" * 60 + "\n")

def print_agent_instructions():
    """Print agent deployment instructions"""
    print("💻 AGENT SETUP (Student Workstations)")
    print("-" * 60)
    print("""
Run on EACH student computer:

1. Open Terminal/Command Prompt
2. Navigate to project: cd lab_manager
3. Install dependencies: pip install -r requirements.txt
4. Run agent: python -m agent.main
5. Leave terminal window open
6. Agent will be discoverable on network

Each agent listens on:
  - http://0.0.0.0:8001
""")
    print("-" * 60 + "\n")

def print_network_requirements():
    """Print network requirements"""
    print("🌐 NETWORK REQUIREMENTS")
    print("-" * 60)
    print("""
✓ All machines must be on same network (same subnet)
✓ Example: 192.168.1.0/24 (192.168.1.1 - 192.168.1.254)
✓ Firewall ports must be open:
  - Port 8000: Server port
  - Port 8001: Agent port
✓ Network should allow TCP connections between machines

Network Architecture:
┌─────────────────────────────────────────────┐
│ Teacher PC (Server) - {ip}:8000           │
│  - GUI Application                          │
│  - FastAPI Server                           │
│  - Discovery Service                        │
└─────────────────────────────────────────────┘
         ↓ Discover & Control
    ┌────┴────┬─────────┬──────────┐
    ↓         ↓         ↓          ↓
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│PC1   │  │PC2   │  │PC3   │  │PC... │
│:8001 │  │:8001 │  │:8001 │  │:8001 │
└──────┘  └──────┘  └──────┘  └──────┘
(Agents)
""".format(ip=get_local_ip()))
    print("-" * 60 + "\n")

def print_troubleshooting():
    """Print troubleshooting guide"""
    print("🔧 TROUBLESHOOTING")
    print("-" * 60)
    print("""
Problem: Agents not discovered
Solution:
  1. Check agents are running: python -m agent.main
  2. Check port 8001 is open: nc -zv <agent_ip> 8001
  3. Check firewall settings
  4. Run: python test_network.py

Problem: Server won't start
Solution:
  1. Check Python 3.8+: python --version
  2. Install deps: pip install -r requirements.txt
  3. Check port 8000: lsof -i :8000 (macOS/Linux)
  4. Kill process: kill -9 <pid>

Problem: Slow discovery
Solution:
  1. Use wired connection (Ethernet) instead WiFi
  2. Reduce network scan timeout in code
  3. Scan specific IP range instead of /24

Problem: Commands don't work
Solution:
  1. Check agent is still running
  2. Check network connectivity: ping <agent_ip>
  3. Check firewall on agent machine
  4. Look at agent logs
""")
    print("-" * 60 + "\n")

def print_security_notes():
    """Print security recommendations"""
    print("🔒 SECURITY NOTES")
    print("-" * 60)
    print("""
⚠️  IMPORTANT for production environments:

Current Implementation (Development):
  - HTTP protocol (unencrypted)
  - Simple token authentication
  - No encryption

Production Recommendations:
  1. Use HTTPS instead of HTTP
     - Generate SSL certificates
     - Use mkcert for local testing
  
  2. Implement proper authentication
     - OAuth2 / OpenID Connect
     - JWT tokens with expiration
     - Role-based access control
  
  3. Network security
     - Restrict to school network only
     - Use VPN for remote access
     - Implement firewall rules
  
  4. Data protection
     - Encrypt data in transit
     - Hash sensitive information
     - Implement audit logging
  
  5. Regular maintenance
     - Update dependencies
     - Monitor logs for attacks
     - Regular security audits
""")
    print("-" * 60 + "\n")

def print_next_steps():
    """Print next steps"""
    print("📋 NEXT STEPS")
    print("-" * 60)
    print("""
1. ✅ Review this information
2. ✅ Read QUICK_START.md for overview
3. ✅ Read NETWORK_SETUP_RU.md for detailed guide
4. ✅ Set up server on teacher's machine
5. ✅ Set up agents on student computers
6. ✅ Test with python test_network.py
7. ✅ Perform test run before production
8. ⏳ Add HTTPS security (future)
9. ⏳ Add OAuth2 authentication (future)

Documentation Files:
  - QUICK_START.md - Quick start guide
  - NETWORK_SETUP_RU.md - Full network setup (Russian)
  - NETWORK_SETUP_EN.md - Full network setup (English)
  - FIRST_RUN.md - First run checklist
  - CHANGES_SUMMARY_RU.md - What was changed

Test & Diagnostics:
  - python test_network.py - Network connectivity test
  - python -m server.api - Run server directly (no GUI)
  - python -m agent.main - Run agent directly
""")
    print("-" * 60 + "\n")

def main():
    """Main function"""
    print_banner()
    print_system_info()
    print_server_instructions()
    print_agent_instructions()
    print_network_requirements()
    print_troubleshooting()
    print_security_notes()
    print_next_steps()

    print("=" * 60)
    print("  🎯 Ready to deploy? Start with QUICK_START.md")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

