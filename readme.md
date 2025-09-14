# OtakuWalL – Smart Dynamic Anime Wallpaper Genarator

OtakuWalL is a smart desktop wallpaper generator that:
- Fetches HD anime wallpapers (You can even get your favorite anime one's or random Too)
- Gets quote for Motivation (From your favorite anime or random based on api)
- Displays dynamic time-based greetings 
- Shows current weather and temperature


## 🔧 Setup Instructions

1. Clone the repo
```bash
git clone https://github.com/bbheemara/OtakuWalL.git
cd OtakuWalL
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Change according to your need
 
   In main.py change
   
   anime_name='your fav anime' (optional)
   
   also change
   
   city='your_city' for weather (Sign up for https://openweathermap.org/ and get your api key it's free and paste in .env)
   
   and If you want to change font of your choice just download your font and save in assets/fonts folder then in main.py FONT_PATH = 'assets/fonts/<your_font>'


5. Run the app and schedule the script 
   ```bash
   python main.py
   ```

<img width="1919" height="1028" alt="Screenshot 2025-07-28 193149" src="https://github.com/user-attachments/assets/bf4ca6ad-b9ee-48d8-a3ed-ab518f4820cc" />