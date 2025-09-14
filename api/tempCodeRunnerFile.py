from fetch_quote import quotes
import requests


quote, anime, character = quotes()

def wallpaper(character_name):
    url = f'https://api.jikan.moe/v4/characters?q={character_name}&limit=1'
    resp=requests.get(url)
    data=resp.json()
    if data["data"]:
        character_data = data["data"][0]
        image_url = character_data["images"]["jpg"]["image_url"]

        print("Character:", character_data["name"])
        print("Image URL:", image_url)
    else:
        print(f"No image found for character: {character_name}")



wallpaper(character)
