import ctypes
import os
import requests
from PIL import Image, ImageDraw, ImageFont 
from greeting.time_greeting import getMessage
from api.fetch_quote import quotes
from api.fetch_quote import movie_quotes
from api.fetch_quote import nature_quote
from dotenv import load_dotenv
from io import BytesIO
import random

def set_wallpaper(type="Anime",quote_type=None,category="Anime",city="Mumbai",use_time_greetings=True):
        load_dotenv()

        SPI_SETDESKWALLPAPER = 20
        SAVE_DIR = 'assets/backgrounds'
        WALLPAPER_FILENAME = 'wallpaper.jpg'
        FONT_PATH = 'assets/fonts/google_font.ttf'
        font=ImageFont.truetype(FONT_PATH,size=50)
        os.makedirs(SAVE_DIR, exist_ok=True)
        message = getMessage()


        try:
            if quote_type=="None":
                 quote = None
                 anime_name = anime_name
                 character = character
            elif type == "Anime":
                quote, anime_name, character = quotes()
            elif type == "Movie":
                quote, movie_name,character = movie_quotes()
            elif type == "Nature":
                 quote, character = nature_quote()
        except Exception as e:
            print("Failed to fetch quote:", e)

            if type == "Anime":
                quote = "I'm not gonna run away, I never go back on my word! That's my nindo: my ninja way!"
                anime_name = "Naruto"
                character = "Naruto Uzumaki" 

            elif type == "Movie" or movie_name:
                quotes_list = ["I'm gonna make him an offer he can't refuse. — Vito Corleone",

                        "May the Force be with you. — Han Solo",

                        "Here's looking at you, kid. — Rick Blaine",

                        "You talkin' to me? — Travis Bickle",

                        "I'll be back — The Terminator (T-800)",

                        "You can't handle the truth! — Col. Nathan R. Jessep",

                        "Frankly, my dear, I don't give a damn. — Rhett Butler",

                        "I see dead people. — Cole Sear",

                        "Here's Johnny! — Jack Torrance",

                        "Life is like a box of chocolates. You never know what you're gonna get. — Forrest Gump"
                                        ]
                movies = [
                "The Godfather",
                "The Shawshank Redemption",
                "The Dark Knight",
                "Pulp Fiction",
                "The Lord of the Rings: The Return of the King",
                "Star Wars: Episode IV - A New Hope",
                "Schindler's List",
                "Forrest Gump",
                "Inception",
                "Casablanca", 
]
                quote = random.choice(quotes_list)


                movie_name = random.choice(movies)
                character = ""

            elif quote_type == "None":
                quote = ""
                anime_name = ""
                character = "" 
        # anime_name=anime_name


        def download_wallpaper(image_url, filename=WALLPAPER_FILENAME, save_dir=SAVE_DIR):
            response = requests.get(image_url)
            if response.status_code == 200:
                filepath = os.path.join(save_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
            else:
                print("Failed to download wallpaper.")
                return None   



        def fetch_wallpaper():
            if  type == "Nature":
                url = f'https://wallhaven.cc/api/v1/search?q=nature&categories=nature&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
            elif   type == "Anime":
                url = f'https://wallhaven.cc/api/v1/search?q={anime_name}&categories=anime&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
            elif type == "Movie":
                url = f'https://wallhaven.cc/api/v1/search?q={movie_name}&categories=movie&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'

            resp = requests.get(url)
            data = resp.json()
            if 'data' in data and len(data['data']) > 0:
                image_url = data['data'][0]['path']
                return download_wallpaper(image_url)
            else:
                print("No wallpaper found:Retrting")
                resp = requests.get(url)
                data = resp.json()
                if 'data' in data and len(data['data']) > 0:
                    image_url = data['data'][0]['path']
                    return download_wallpaper(image_url)
                


        def wrap_text(text, font, max_width, draw):
            words = text.split()
            lines = []
            line = ""

            for word in words:
                test_line = f"{line} {word}".strip()
                bbox = draw.textbbox((0, 0), test_line, font=font)
                w = bbox[2] - bbox[0]
                if w <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            if line:
                lines.append(line)
            return lines



        def draw_outline_text(draw, text, position, font, fill=(255,255,255), outline=(0,0,0)):
            x, y = position
            for dx in [-2, 0, 2]:
                for dy in [-2, 0, 2]:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline)
            draw.text((x, y), text, font=font, fill=fill)



        def draw_wrapped_text(draw, text, position, font, max_width):
            x, y = position
            lines = wrap_text(text, font, max_width, draw)
            for line in lines:
                draw_outline_text(draw, line, (x, y), font)
                bbox = draw.textbbox((x, y), line, font=font)
                line_height = bbox[3] - bbox[1]
                y += line_height + 5


        downloaded_path = fetch_wallpaper()
        if not downloaded_path:
            exit()


        image = Image.open(downloaded_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_PATH, 50)

        if use_time_greetings == True:
          draw_wrapped_text(draw, message, (100, 40), font, image.width - 60)
        
        if quote_type == "None":
            quote_text = ""
        else: 

            quote_text = f'"{quote}"\n- {character}'
        quote_lines = wrap_text(quote_text, font, image.width - 100, draw)


        line_heights = [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in quote_lines]
        total_quote_height = sum(line_heights) + 5 * (len(quote_lines) - 1)

        start_y =  image.height - total_quote_height - 100




        for i, line in enumerate(quote_lines):
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            x = (image.width - line_width) // 2
            draw_outline_text(draw, line, (x, start_y), font)
            start_y += line_heights[i] + 5            

        image = image.convert('RGBA') 
        API_KEY=os.environ.get('api')
        city=city
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        resp_w=requests.get(url)
        data_w=resp_w.json()

        if resp_w.status_code==200:
            temp=data_w['main']['temp']
            weather_state=data_w['weather'][0]['main']
            icon_code=data_w['weather'][0]['icon']
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            resp=requests.get(icon_url)
            icon_img = Image.open(BytesIO(resp.content)).convert("RGBA")
            

            temp=temp
            temp_text=f'{temp}°C'
            if weather_state=='Clouds':
            
            #    weather = Image.open('assets/clouds.png').convert("RGBA") 
                icon_img = icon_img.resize((50, 50))
                alpha =200
                icon_img.putalpha(alpha)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)  
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw,temp_text, (image.width-400,50),font,image.width-60)

            elif weather_state=='Clear':
                icon_img = icon_img.resize((50, 50))
                alpha =200
                icon_img.putalpha(alpha)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)  
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw,temp_text, (image.width-400,50),font,image.width-60)

            elif weather_state=='Rain':
                icon_img = icon_img.resize((50, 50))
                alpha =200
                icon_img.putalpha(alpha)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)  
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw,temp_text, (image.width-400,50),font,image.width-60)


            elif weather_state=='Drizzle':
                    icon_img = icon_img.resize((50, 50))
                    alpha =200
                    icon_img.putalpha(alpha)
                    draw = ImageDraw.Draw(image)
                    image.paste(icon_img, (image.width-200, 50), icon_img)  
                    draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                    draw_wrapped_text(draw,temp_text, (image.width-400,50),font,image.width-60)

            elif weather_state=='Snow':
                        icon_img = icon_img.resize((50, 50))
                        alpha =200
                        icon_img.putalpha(alpha)
                        draw = ImageDraw.Draw(image)
                        image.paste(icon_img, (image.width-200, 50), icon_img)  
                        draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                        draw_wrapped_text(draw,temp_text, (image.width-400,50),font,image.width-60)


        else:
            print("Error:", data_w['message'])


        bmp_path = downloaded_path.replace('.jpg', '.bmp')
        image.save(bmp_path, 'BMP')
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(bmp_path), 3)
        pass