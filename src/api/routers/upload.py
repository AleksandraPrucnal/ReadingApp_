from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid
from src.config import config

router = APIRouter(tags=["Upload"])


@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """
    Przyjmuje plik obrazka, zapisuje go na serwerze i zwraca URL.
    """
    # 1. Walidacja (czy to na pewno obrazek?)
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="Plik musi być obrazkiem")

    # 2. Generowanie unikalnej nazwy (żeby 'kot.jpg' nie nadpisał innego 'kot.jpg')
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    file_location = f"uploaded_images/{unique_filename}"

    # 3. Zapisywanie pliku na dysku
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # 4. Generowanie URL (adresu), który zapiszesz w bazie
    # Uwaga: W produkcji base_url powinien być domeną, w dev to localhost
    # Dla emulatora Androida to 10.0.2.2, dla PC localhost.
    # Zwracamy ścieżkę relatywną, a frontend doklei sobie domenę,
    # LUB zwracamy pełny URL jeśli masz zmienną BASE_URL w configu.

    # Wersja bezpieczna (zwraca ścieżkę statyczną):
    image_url = f"/static/{unique_filename}"

    return {"url": image_url}