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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def set_wallpaper(type="Anime", quote_type=None, custom_quote=None, custom_path=None,
                  category="Anime", city="Mumbai", use_time_greetings=True, genre=""):
    try:
        load_dotenv()

        SPI_SETDESKWALLPAPER = 20
        SAVE_DIR = os.path.join(BASE_DIR, 'assets', 'backgrounds')
        WALLPAPER_FILENAME = 'wallpaper.jpg'
        FONT_PATH = os.path.join(BASE_DIR, 'assets', 'fonts', 'google_font.ttf')
        os.makedirs(SAVE_DIR, exist_ok=True)

        font = ImageFont.truetype(FONT_PATH, size=50)
        message = getMessage()
        movie_name = ""
        anime_name = ""
        character = ""
        quote = ""
        downloaded_path = None

        monitors = get_monitors()
        if not monitors:
            screen_w, screen_h = 1920, 1080
        else:
            monitor = monitors[0]
            screen_w, screen_h = monitor.width, monitor.height

        try:
            if quote_type == "None":
                quote = ""
            elif type == "Anime":
                quote, anime_name, character = quotes()
            elif type == "Movie":
                quote, movie_name, character = movie_quotes()
            elif type == "Nature":
                quote, character = nature_quote()
            elif type == "custom":
                quote = custom_quote or ""
                character = ""
                anime_name = ""
        except Exception as e:

            print("Failed to fetch quote:", e)
            if type == "Anime":
                quote = "I'm not gonna run away..." 
                anime_name = "Naruto"
                character = "Naruto Uzumaki"
            elif type == "Movie":
                quotes_list = [
                    "I'm gonna make him an offer he can't refuse. — Vito Corleone",
                    "May the Force be with you. — Han Solo",
                    "Here's looking at you, kid. — Rick Blaine",
                ]
                quote = random.choice(quotes_list)
                movie_name = "Inception"
                character = ""

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
            if image.width * image.height < 500 * 500:
                resample_method = Image.Resampling.BILINEAR
            else:
                resample_method = Image.Resampling.LANCZOS
            image_ratio = image.width / image.height
            screen_ratio = max_w / max_h
            if image_ratio > screen_ratio:
                new_width = max_w
                new_height = int(max_w / image_ratio)
            else:
                new_height = max_h
                new_width = int(max_h * image_ratio)
            return image.resize((new_width, new_height), resample_method)

        def download_wallpaper(image_url, filename=WALLPAPER_FILENAME, save_dir=SAVE_DIR):
            resp = requests.get(image_url, timeout=10)
            if resp.status_code == 200:
                filepath = os.path.join(save_dir, filename)
                with open(filepath, 'wb') as fh:
                    fh.write(resp.content)
                return filepath
            else:
                print("Failed to download wallpaper:", resp.status_code)
                return None

        def fetch_wallpaper():

            if type == "Nature":
                url = 'https://wallhaven.cc/api/v1/search?q=nature&categories=nature&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
            elif type == "Anime":
                url = f'https://wallhaven.cc/api/v1/search?q={anime_name or "anime"}&categories=anime&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
            elif type == "Movie":
                url = f'https://wallhaven.cc/api/v1/search?q={movie_name or "movie"}&categories=movie&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
            elif type == "type a genre":
                url = f'https://wallhaven.cc/api/v1/search?q={genre}&sorting=random&categories=111&purity=100&atleast=1920x1080'
                resp = requests.get(url, timeout=5)
                data = resp.json() 
                if 'data' in data and len(data['data'])  < 0:
                   url = f'https://wallhaven.cc/api/v1/search?q=anime&categories=anime&purity=100&sorting=random&resolutions=1920x1080&ratios=16x9'
                

                

            else:
                url = None

            if not url:
                return None

            resp = requests.get(url, timeout=5)
            data = resp.json() if resp.status_code == 200 else {}
            if 'data' in data and len(data['data']) > 0:
                image_url = data['data'][0].get('path') or data['data'][0].get('file')
                if image_url:
                    return download_wallpaper(image_url)

            print("No wallpaper found from API")
            return None

        def wrap_text(text, font_obj, max_width, draw_obj):
            words = text.split()
            lines = []
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                bbox = draw_obj.textbbox((0, 0), test_line, font=font_obj)
                w = bbox[2] - bbox[0]
                if w <= max_width:
                    line = test_line
                else:
                    if line:
                        lines.append(line)
                    line = word
            if line:
                lines.append(line)
            return lines

        def draw_outline_text(draw_obj, text, position, font_obj, fill=(255, 255, 255), outline=(0, 0, 0)):
            x, y = position
            for dx in [-2, 0, 2]:
                for dy in [-2, 0, 2]:
                    draw_obj.text((x + dx, y + dy), text, font=font_obj, fill=outline)
            draw_obj.text((x, y), text, font=font_obj, fill=fill)

        def draw_wrapped_text(draw_obj, text, position, font_obj, max_width):
            x, y = position
            lines = wrap_text(text, font_obj, max_width, draw_obj)
            for line in lines:
                draw_outline_text(draw_obj, line, (x, y), font_obj)
                bbox = draw_obj.textbbox((x, y), line, font=font_obj)
                line_height = bbox[3] - bbox[1]
                y += line_height + 5


        if custom_path:
            image = Image.open(custom_path).convert("RGB").copy()
        else:
            downloaded_path = fetch_wallpaper()
            if not downloaded_path:
                print("No wallpaper could be fetched, aborting.")
                return
            image = Image.open(downloaded_path).convert("RGB")

        draw = ImageDraw.Draw(image)

        if use_time_greetings:
            draw_wrapped_text(draw, message, (100, 40), font, image.width - 60)


        if type == "custom":
            quote_text = custom_quote or ""
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
            line_heights = []
            for line in quote_lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_heights.append(bbox[3] - bbox[1])
            total_quote_height = sum(line_heights) + 5 * (len(quote_lines) - 1)
            start_y = image.height - total_quote_height - 100
            for i, line in enumerate(quote_lines):
                line_bbox = draw.textbbox((0, 0), line, font=font)
                line_width = line_bbox[2] - line_bbox[0]
                x = (image.width - line_width) // 2
                draw_outline_text(draw, line, (x, start_y), font)
                start_y += line_heights[i] + 5


        API_KEY = os.environ.get('api')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        try:
            resp_w = requests.get(url, timeout=8)
            data_w = resp_w.json()
        except Exception as e:
            resp_w = None
            data_w = {}
            print("Weather request failed:", e)

        if resp_w and resp_w.status_code == 200 and 'main' in data_w:
            temp = data_w['main'].get('temp')
            weather_state = data_w.get('weather', [{}])[0].get('main', '')
            icon_code = data_w.get('weather', [{}])[0].get('icon', '')
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            try:
                resp = requests.get(icon_url, timeout=5)
                icon_img = Image.open(BytesIO(resp.content)).convert("RGBA")
                icon_img = icon_img.resize((50, 50))
                icon_img.putalpha(200)
                image.paste(icon_img, (image.width - 200, 50), icon_img)
                temp_text = f'{temp}°C' if temp is not None else ''
                draw_wrapped_text(draw, weather_state, (image.width - 400 + 50, 100), font, image.width - 60)
                draw_wrapped_text(draw, temp_text, (image.width - 400, 50), font, image.width - 60)
            except Exception as e:
                print("Failed to paste weather icon:", e)
        else:
            print("Weather API error:", data_w.get('message', 'unknown'))

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


        
    except Exception as exc:

        print("Exception in set_wallpaper:", exc)
        raise
