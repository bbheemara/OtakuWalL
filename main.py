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
from screeninfo import get_monitors
import winreg


def set_wallpaper(type="Anime",quote_type=None,custom_quote=None,custom_path=None,category="Anime",city="Mumbai",use_time_greetings=True):
        load_dotenv()

        SPI_SETDESKWALLPAPER = 20
        SAVE_DIR = 'assets/backgrounds'
        WALLPAPER_FILENAME = 'wallpaper.jpg'
        FONT_PATH = 'assets/fonts/google_font.ttf'
        font=ImageFont.truetype(FONT_PATH,size=50)
        os.makedirs(SAVE_DIR, exist_ok=True)
        message = getMessage()
        movie_name = ""
        anime_name = ""
        character = ""
        quote = ""
        downloaded_path=""
        monitor = get_monitors()[0]
        screen_w = monitor.width
        screen_h = monitor.height
        try:
            if quote_type == "None":
                quote = ""
                anime_name = anime_name
                character = character
            elif type == "Anime":
                quote, anime_name, character = quotes()
            elif type == "Movie":
                quote, movie_name, character = movie_quotes()
            elif type == "Nature":  
                quote, character = nature_quote()
            elif type == "custom":
                quote = custom_quote if custom_quote else ""
                character = ""
                anime_name = ""
        except Exception as e:
            print("Failed to fetch quote:", e)
            if type == "Anime":
                quote = "I'm not gonna run away, I never go back on my word! That's my nindo: my ninja way!"
                anime_name = "Naruto"
                character = "Naruto Uzumaki"

            elif type == "Movie":
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
        def set_wallpaper_style_fit():
            reg_path = r"Control Panel\Desktop"
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(reg_key, "WallpaperStyle", 0, winreg.REG_SZ, "6")
                winreg.SetValueEx(reg_key, "TileWallpaper", 0, winreg.REG_SZ, "0")
                winreg.CloseKey(reg_key)

            except Exception as e:
                print("Failed to set wallpaper style:", e)

        def resize_custom_img(image, max_w, max_h):
            if image.width * image.height < 500*500:  
               resample_method = Image.Resampling.BILINEAR  
            else:
               resample_method = Image.Resampling.LANCZOS   
            image_ratio = image.width / image.height
            screen_ratio = max_w/max_h

            if image_ratio > screen_ratio:
                new_width = max_w
                new_height = int(max_w / image_ratio) 
            else:
                new_height = max_h
                new_width = int(max_h * image_ratio)    
            return image.resize((new_width, new_height), resample_method)
            
        
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
                
                resp = requests.get(url,timeout=5
                                    )
                data = resp.json()
                if 'data' in data and len(data['data']) > 0:
                    image_url = data['data'][0]['path']
                    return download_wallpaper(image_url)
                else:
                    print("No wallpaper found:Retrting")
                    resp = requests.get(url,timeout=5)
                    data = resp.json()
                    if 'data' in data and len(data['data']) > 0:
                        image_url = data['data'][0]['path']
                        return download_wallpaper(image_url)
                    
            elif   type == "Anime":
                url = f'https://wallhaven.cc/api/v1/search?q={anime_name}&categories=anime&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
                
                resp = requests.get(url,timeout=5)
                data = resp.json()
                if 'data' in data and len(data['data']) > 0:
                    image_url = data['data'][0]['path']
                    return download_wallpaper(image_url)
                else:
                    print("No wallpaper found:Retrting")
                    resp = requests.get(url,timeout=5)
                    data = resp.json()
                    if 'data' in data and len(data['data']) > 0:
                        image_url = data['data'][0]['path']
                        return download_wallpaper(image_url)
                
            elif type == "Movie":
                url = f'https://wallhaven.cc/api/v1/search?q={movie_name}&categories=movie&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'

                resp = requests.get(url,timeout=5)
                data = resp.json()
                if 'data' in data and len(data['data']) > 0:
                    image_url = data['data'][0]['path']
                    return download_wallpaper(image_url)
                else:
                    print("No wallpaper found:Retrting")
                    resp = requests.get(url,timeout=5)
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


        if custom_path:
            image = Image.open(custom_path).convert("RGB").copy()





        else:
            downloaded_path = fetch_wallpaper()
            if not downloaded_path:
               exit()
            image = Image.open(downloaded_path).convert("RGB")

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_PATH, 50)

        if use_time_greetings == True:
          draw_wrapped_text(draw, message, (100, 40), font, image.width - 60)
                
        
        if type == "custom":
            quote_text = custom_quote if custom_quote else ""
        elif quote_type == "None" or quote_type is None:
            quote_text = ""
        else:
            if quote and character:
                quote_text = f'"{quote}"\n- {character}'
            elif quote:
                quote_text = f'"{quote}"'
            else:
                quote_text = ""

        if quote_text.strip():
            quote_lines = wrap_text(quote_text, font, image.width - 100, draw)
            line_heights = [draw.textbbox((0,0), line, font=font)[3] - draw.textbbox((0,0), line, font=font)[1] for line in quote_lines]
            total_quote_height = sum(line_heights) + 5 * (len(quote_lines) - 1)
            start_y = image.height - total_quote_height - 100
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
        resp_w=requests.get(url,timeout=5)
        data_w=resp_w.json()

        if resp_w.status_code==200:
            temp=data_w['main']['temp']
            weather_state=data_w['weather'][0]['main']
            icon_code=data_w['weather'][0]['icon']
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            resp=requests.get(icon_url,timeout=2)
            icon_img = Image.open(BytesIO(resp.content)).convert("RGBA")
            

            temp=temp
            temp_text=f'{temp}°C'
            if weather_state == 'Thunderstorm':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Drizzle':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Rain':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Snow':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Mist':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Smoke':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Haze':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Dust':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Fog':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Sand':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Ash':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Squall':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Tornado':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Clear':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)

            elif weather_state == 'Clouds':
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                draw = ImageDraw.Draw(image)
                image.paste(icon_img, (image.width-200, 50), icon_img)
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width-400,50), font, image.width-60)


        else:
            print("Error:", data_w['message'])

        if image.mode == 'RGBA':
            image = image.convert('RGB')

        image = resize_custom_img(image, screen_w, screen_h)

        if custom_path:
            dir_path = os.path.dirname(custom_path)
            base_name = os.path.basename(custom_path)
            name_without_ext = os.path.splitext(base_name)[0]
            save_path = os.path.join(dir_path, f"{name_without_ext}_wallpaper.bmp")
            
            set_wallpaper_style_fit()
   
            image.save(save_path, 'BMP')
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(save_path), 3)

        else:
            bmp_path = os.path.join(SAVE_DIR, 'wallpaper.bmp')
            
            image.save(bmp_path, 'BMP')
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(bmp_path), 3)

