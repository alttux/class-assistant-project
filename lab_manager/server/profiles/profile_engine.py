import json
import os
from ..api_client import APIClient
from shared import schemas

class ProfileEngine:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.profiles_dir = os.path.join(os.path.dirname(__file__), "default_profiles")

    async def apply_profile_to_workstation(self, ip: str, profile_name: str):
        profile_path = os.path.join(self.profiles_dir, f"{profile_name}.json")
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                settings = json.load(f)
            # Send apply_profile command with params
            cmd = schemas.CommandRequest(command="apply_profile", params={"profile": profile_name})
            await self.api_client.send_command(ip, cmd)
        else:
            raise ValueError("Profile not found")

    async def apply_profile_to_all(self, workstations: list, profile_name: str):
        for ip in workstations:
            await self.apply_profile_to_workstation(ip, profile_name)
