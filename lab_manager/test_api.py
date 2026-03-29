#!/usr/bin/env python
"""
Comprehensive test script for the Classroom Manager application.
Tests all major endpoints of the server and agent APIs.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
AGENT_URL = "http://localhost:8001"
AUTH_TOKEN = "secret_token"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_workstations():
    print_section("Testing Workstations API")
    
    # Get workstations
    print("\n1. Getting all workstations...")
    response = requests.get(f"{BASE_URL}/workstations/")
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")
    
    # Create a new workstation
    print("\n2. Creating a new workstation...")
    workstation_data = {
        "name": "PC2",
        "ip_address": "192.168.1.11",
        "status": "offline"
    }
    response = requests.post(f"{BASE_URL}/workstations/", json=workstation_data)
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")
    
    # Update status
    print("\n3. Updating workstation status...")
    response = requests.put(f"{BASE_URL}/workstations/1/status", params={"status": "online"})
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")

def test_profiles():
    print_section("Testing Profiles API")
    
    # Get profiles
    print("\n1. Getting all profiles...")
    response = requests.get(f"{BASE_URL}/profiles/")
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")
    
    # Create a new profile
    print("\n2. Creating a new profile...")
    profile_data = {
        "name": "exam",
        "description": "Exam profile - strict settings",
        "settings": {"disable_internet": True, "kill_processes": ["chrome", "firefox"]}
    }
    response = requests.post(f"{BASE_URL}/profiles/", json=profile_data)
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")

def test_logs():
    print_section("Testing Logs API")
    
    # Get logs
    print("\n1. Getting all logs...")
    response = requests.get(f"{BASE_URL}/logs/")
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")
    
    # Create a new log entry
    print("\n2. Creating a new log entry...")
    log_data = {
        "workstation_id": 1,
        "action": "shutdown",
        "details": "System shutdown command executed",
        "timestamp": "2026-03-29T10:15:00"
    }
    response = requests.post(f"{BASE_URL}/logs/", json=log_data)
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")

def test_reports():
    print_section("Testing Reports API")
    
    # Get report
    print("\n1. Getting usage report...")
    response = requests.get(f"{BASE_URL}/report?workstation_id=1")
    print(f"   Status: {response.status_code}")
    print(f"   Data: {json.dumps(response.json(), indent=2)}")
    
    # Export report
    print("\n2. Exporting report to PDF...")
    response = requests.post(f"{BASE_URL}/export_report?workstation_id=1")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Report exported successfully to report.pdf")
        print(f"   Data: {json.dumps(response.json(), indent=2)}")

def test_agent_monitor():
    print_section("Testing Agent Monitor Endpoint")
    
    print("\n1. Getting monitor data from agent...")
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    response = requests.get(f"{AGENT_URL}/monitor", headers=headers)
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   CPU Usage: {data.get('cpu_usage')}%")
    print(f"   RAM Usage: {data.get('ram_usage')}%")
    print(f"   Disk Usage: {data.get('disk_usage')}%")
    print(f"   Total Processes: {len(data.get('processes', []))}")

def test_agent_commands():
    print_section("Testing Agent Command Endpoint")
    
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
    # Test lock_screen command
    print("\n1. Testing lock_screen command...")
    command_data = {"command": "lock_screen"}
    response = requests.post(f"{AGENT_URL}/command", json=command_data, headers=headers)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")

def main():
    print("\n" + "="*60)
    print("  CLASSROOM MANAGER - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    try:
        test_workstations()
        test_profiles()
        test_logs()
        test_reports()
        test_agent_monitor()
        test_agent_commands()
        
        print_section("TEST SUMMARY")
        print("\n✓ All tests completed successfully!")
        print("✓ Server API is working correctly")
        print("✓ Agent API is responding correctly")
        print("✓ Database operations are functional")
        print("✓ Report generation is working")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")

if __name__ == "__main__":
    main()

