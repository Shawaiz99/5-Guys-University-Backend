import os
from dotenv import load_dotenv
from pathlib import Path
import cloudinary
import cloudinary.uploader

# Загрузка .env
env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

# Проверка, что переменные загружаются
print("DEBUG: cloud_name =", os.getenv("CLOUDINARY_CLOUD_NAME"))
print("DEBUG: api_key =", os.getenv("CLOUDINARY_API_KEY"))
print("DEBUG: api_secret =", os.getenv("CLOUDINARY_API_SECRET"))

# Настройка cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_image_to_cloudinary(file):
    result = cloudinary.uploader.upload(file)
    return result["secure_url"]