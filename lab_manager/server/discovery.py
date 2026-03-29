import socket
import ipaddress

def discover_agents(network: str = "192.168.1.0/24"):
    """Simple network scan to find agents. In production, use better discovery."""
    agents = []
    net = ipaddress.ip_network(network)
    for ip in net.hosts():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((str(ip), 8001))  # AGENT_PORT
            if result == 0:
                agents.append(str(ip))
            sock.close()
        except:
            pass
    return agents
