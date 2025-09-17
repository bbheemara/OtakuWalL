import os
import json
from main import set_wallpaper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "scheduler_config.json")


def load_scheduler_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {}

if __name__ == "__main__":
    config = load_scheduler_config()
    try:
        if config.get("schedule_enabled", False):
            set_wallpaper(
                type=config.get("wallpaper_type", "Anime"),
                quote_type=config.get("quote_type", None),
                custom_quote=config.get("custom_quote"),
                custom_path=config.get("custom_path"),
                category=config.get("wallpaper_type", "Anime"),
                city=config.get("city", "Mumbai"),
                use_time_greetings=config.get("use_time_greetings", True),
                genre=config.get("genre", "")
            )
        
    except Exception as e:
        print(e)
