import httpx
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

THECATAPI_BASE_URL = os.getenv("THECATAPI_BASE_URL", "https://api.thecatapi.com/v1")


async def validate_breed(breed: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{THECATAPI_BASE_URL}/breeds")
            response.raise_for_status()
            breeds = response.json()
            
            breed_lower = breed.lower()
            for api_breed in breeds:
                if api_breed.get("name", "").lower() == breed_lower:
                    return True
            return False
    except Exception as e:
        print(f"Error validating breed: {e}")
        return False
