import httpx

class ArasaacService:
    BASE_URL = 'https://api.arasaac.org/v1/pictograms/es/'

    @staticmethod
    async def fetch_pictogram_data(pictogram_id):
        url = f'{ArasaacService.BASE_URL}{pictogram_id}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def fetch_pictogram_image(pictogram_id):
        url = f'https://static.arasaac.org/pictograms/{pictogram_id}/{pictogram_id}_2500.png'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.url

    @staticmethod
    async def search_pictograms_by_word(word):
        url = f'{ArasaacService.BASE_URL}search/{word}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_pictogram_id(json_data):
        first_object = json_data[0]
        got_id = first_object['_id']
        return got_id