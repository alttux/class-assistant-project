import subprocess
import platform

def set_proxy(proxy: str):
    if platform.system() == "Windows":
        subprocess.run(["netsh", "winhttp", "set", "proxy", proxy])
    elif platform.system() == "Linux":
        # Set environment or use gsettings
        pass

def block_internet():
    if platform.system() == "Linux":
        subprocess.run(["iptables", "-A", "OUTPUT", "-p", "tcp", "--dport", "80", "-j", "DROP"])
        subprocess.run(["iptables", "-A", "OUTPUT", "-p", "tcp", "--dport", "443", "-j", "DROP"])

def unblock_internet():
    if platform.system() == "Linux":
        subprocess.run(["iptables", "-D", "OUTPUT", "-p", "tcp", "--dport", "80", "-j", "DROP"])
        subprocess.run(["iptables", "-D", "OUTPUT", "-p", "tcp", "--dport", "443", "-j", "DROP"])

def edit_hosts_file(block_sites: list):
    hosts_path = "/etc/hosts" if platform.system() != "Windows" else "C:\\Windows\\System32\\drivers\\etc\\hosts"
    with open(hosts_path, "a") as f:
        for site in block_sites:
            f.write(f"127.0.0.1 {site}\n")
