
import httpx
from httpx import AsyncClient

class ExternalApiArasaac:
    async def search_berry():
        url = 'https://pokeapi.co/api/v2/berry/cheri'
        with httpx.Client() as client:
            response = client.get(url)
            return response.json()