import subprocess
import platform

def set_proxy(proxy: str):
    # Set environment or use gsettings
    pass

def block_internet():
    subprocess.run(["nmcli", "radio", "wifi", "off"])

def unblock_internet():
    subprocess.run(["nmcli", "radio", "wifi", "on"])

def edit_hosts_file(block_sites: list):
    hosts_path = "/etc/hosts"
    with open(hosts_path, "a") as f:
        for site in block_sites:
            f.write(f"127.0.0.1 {site}\n")
