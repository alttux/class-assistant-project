"""
Network discovery and agent discovery module.
Helps find and register agents on the local network.
"""
import socket
import ipaddress
import asyncio
from typing import List, Optional
from .api_client import APIClient

class NetworkDiscovery:
    """Discover agents on the local network"""

    @staticmethod
    def get_local_ip() -> str:
        """Get the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    @staticmethod
    def get_network_range(ip: str, subnet_mask: str = "255.255.255.0") -> str:
        """Get network range from IP and subnet mask"""
        try:
            # Convert IP and mask to network address
            ip_parts = ip.split(".")
            mask_parts = subnet_mask.split(".")

            network_parts = [
                str(int(ip_parts[i]) & int(mask_parts[i]))
                for i in range(4)
            ]
            network = ".".join(network_parts) + "/24"
            return network
        except:
            # Default to Class C network
            return ".".join(ip.split(".")[:3]) + ".0/24"

    @staticmethod
    async def scan_port(host: str, port: int, timeout: int = 2) -> bool:
        """Asynchronously scan if a port is open"""
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False

    @staticmethod
    async def discover_agents(
        network: Optional[str] = None,
        port: int = 8001,
        timeout: int = 2
    ) -> List[str]:
        """
        Discover all agents on the network

        Args:
            network: Network range (e.g., "192.168.1.0/24"). If None, auto-detect.
            port: Port to scan (default: 8001 for agents)
            timeout: Connection timeout in seconds

        Returns:
            List of agent IPs
        """
        agents = []

        # Auto-detect network if not provided
        if network is None:
            local_ip = NetworkDiscovery.get_local_ip()
            network = NetworkDiscovery.get_network_range(local_ip)

        if network is None:
            print("Could not determine network range")
            return agents

        try:
            net = ipaddress.ip_network(network, strict=False)
        except Exception as e:
            print(f"Invalid network: {network} - {str(e)}")
            return agents

        # Scan all IPs in network
        tasks = []
        for ip in net.hosts():
            ip_str = str(ip)
            # Skip the current machine and broadcast
            if ip_str != NetworkDiscovery.get_local_ip():
                tasks.append(NetworkDiscovery._check_agent(ip_str, port, timeout))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if result and isinstance(result, str):
                agents.append(result)

        return sorted(agents)

    @staticmethod
    async def _check_agent(ip: str, port: int, timeout: int) -> Optional[str]:
        """Check if agent is running on this IP"""
        if await NetworkDiscovery.scan_port(ip, port, timeout):
            return ip
        return None

    @staticmethod
    async def verify_agent(ip: str, port: int = 8001) -> bool:
        """Verify that an agent is actually running at this IP"""
        try:
            client = APIClient(f"http://{ip}:{port}")
            # Try to get monitor data as a verification
            response = await client.get_monitor_data(ip)
            return response is not None
        except:
            return False

def discover_agents_sync(
    network: Optional[str] = None,
    port: int = 8001,
    timeout: int = 2
) -> List[str]:
    """
    Synchronous wrapper for agent discovery

    Example:
        agents = discover_agents_sync()
        for agent_ip in agents:
            print(f"Found agent at {agent_ip}")
    """
    return asyncio.run(NetworkDiscovery.discover_agents(network, port, timeout))

