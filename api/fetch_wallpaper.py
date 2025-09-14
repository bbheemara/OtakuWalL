from api.fetch_quote import quotes
import requests
import os
from os import makedirs

quote, anime_name, character = quotes()


def download_wallpaper(image_url,filename='wallpaper.jpg',save_dir='assets/backgrounds'):
    makedirs(save_dir,exist_ok=True)
    response=requests.get(image_url)

    if response.status_code==200:
        filepath=os.path.join(save_dir,filename)

        with open(filepath,'wb') as f:
            f.write(response.content)
        return filepath
    else:
        print("failed to download:)")
   
        return None



def wallpaper():
    url = f'https://wallhaven.cc/api/v1/search?q={anime_name}&categories=anime&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
    resp=requests.get(url)
    data=resp.json()
    if 'data' in data and len(data['data'])>0:
        first_wallp=data['data'][0]
        image_url=first_wallp['path']
        if image_url:
            download_wallpaper(image_url)
    else:
        print("NOT found")      

wallpaper()


    
