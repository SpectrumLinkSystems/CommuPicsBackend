import cloudinary
import os
from dotenv import load_dotenv

class CloudinaryService:
    def __init__(self):
        load_dotenv()
        self.cloudinary = cloudinary
        self.cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True,
        )

    def upload_image(self, image):
        response = self.cloudinary.uploader.upload(image)
        return response

    def delete_image(self, public_id):
        return self.cloudinary.destroy(public_id)
