import httpx
from shared import constants, schemas

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=constants.TIMEOUT)

    async def send_command(self, ip: str, command: schemas.CommandRequest):
        url = f"http://{ip}:{constants.AGENT_PORT}/command"
        headers = {"Authorization": f"Bearer {constants.AUTH_TOKEN}"}
        response = await self.client.post(url, json=command.dict(), headers=headers)
        return response.json()

    async def get_monitor_data(self, ip: str):
        url = f"http://{ip}:{constants.AGENT_PORT}/monitor"
        headers = {"Authorization": f"Bearer {constants.AUTH_TOKEN}"}
        response = await self.client.get(url, headers=headers)
        return response.json()

    async def close(self):
        await self.client.aclose()
