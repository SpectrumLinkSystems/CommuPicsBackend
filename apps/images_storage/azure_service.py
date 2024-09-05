import os
import httpx
from dotenv import load_dotenv, dotenv_values

class AzureService:

    async def upload_file():
        load_dotenv()
        url = "https://api.imgur.com/3/image"

        payload = {
            "type": "image",
            "title": "Simple upload",
            "description": "This is a simple image upload in Imgur",
        }

        files = [
            (
                "image",
                (
                    "milk_photo.jpg",
                    open("/home/DRN-00X/Downloads/milk_photo.jpg", "rb"),
                    "image/jpg",
                ),
            )
        ]

        headers = {"Authorization": os.getenv("IMGUR_CLIENT_ID")}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload, files=files, headers=headers)
            return response.json()
