#!/usr/bin/env python3
"""
Network connectivity test script for Classroom Manager
Tests if agents can be discovered and connected to
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from server.network_discovery import NetworkDiscovery, discover_agents_sync
from shared import constants


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)


def test_local_ip():
    """Test local IP detection"""
    print_header("Testing Local IP Detection")

    local_ip = NetworkDiscovery.get_local_ip()
    print(f"✅ Local IP: {local_ip}")

    if local_ip == "127.0.0.1":
        print("⚠️  Local IP is localhost - network may not be accessible")
    else:
        print(f"✅ Valid network IP detected")

    return local_ip


def test_network_range(local_ip):
    """Test network range detection"""
    print_header("Testing Network Range Detection")

    network = NetworkDiscovery.get_network_range(local_ip)
    print(f"✅ Detected network: {network}")
    return network


def test_port_scan():
    """Test port scanning"""
    print_header("Testing Port Scanning")

    # Test localhost (should be quick)
    print("Testing port 8001 on localhost...")
    result = asyncio.run(NetworkDiscovery.scan_port("127.0.0.1", 8001, timeout=1))
    print(f"  Result: {'Open' if result else 'Closed (expected)'}")

    print("✅ Port scanning works")


async def test_agent_discovery(network):
    """Test agent discovery"""
    print_header("Testing Agent Discovery")

    print(f"Scanning network: {network}")
    print("(This may take 30-60 seconds depending on network size)")
    print("")

    agents = await NetworkDiscovery.discover_agents(network=network, timeout=1)

    if agents:
        print(f"✅ Found {len(agents)} agent(s):")
        for agent_ip in agents:
            print(f"   - {agent_ip}")
    else:
        print("⚠️  No agents found")
        print("   Make sure:")
        print("   1. Agent is running: python -m agent.main")
        print("   2. Port 8001 is open in firewall")
        print("   3. Agents are on the same network")

    return agents


def test_constants():
    """Test constants configuration"""
    print_header("Testing Constants Configuration")

    print(f"SERVER_HOST: {constants.SERVER_HOST}")
    print(f"SERVER_IP: {constants.SERVER_IP}")
    print(f"DEFAULT_PORT: {constants.DEFAULT_PORT}")
    print(f"AGENT_PORT: {constants.AGENT_PORT}")
    print(f"AUTH_TOKEN: {'***' if constants.AUTH_TOKEN else 'Not set'}")

    print("✅ Constants loaded correctly")


def main():
    """Main test function"""
    print("\n")
    print("  🎓 Classroom Manager - Network Connectivity Test")
    print("\n")

    try:
        # Test constants
        test_constants()

        # Test local IP
        local_ip = test_local_ip()

        # Test network range
        network = test_network_range(local_ip)

        # Test port scanning
        test_port_scan()

        # Test agent discovery
        print_header("Running Full Agent Discovery")
        agents = asyncio.run(test_agent_discovery(network))

        # Summary
        print_header("Test Summary")
        print("\n✅ All tests completed!")
        print(f"\nFound agents: {len(agents)}")

        if agents:
            print("\n✅ Network is configured correctly!")
            print("You can now use the Classroom Manager GUI:")
            print("  python -m server.gui.main_window")
        else:
            print("\n⚠️  No agents found on network")
            print("Troubleshooting steps:")
            print("1. Make sure agent.main is running on workstations")
            print("2. Check firewall settings (port 8001)")
            print("3. Verify all machines are on same network")
            print("4. Check network connectivity with: ping <ip>")

        print("\n")
        return 0

    except Exception as e:
        print_header("Error Occurred")
        print(f"❌ {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

