import requests  
import random



def quotes():
    url= 'https://api.animechan.io/v1/quotes/random'
    resp=requests.get(url)
    data=resp.json()
    quote=data['data']['content']
    anime_name=data['data']['anime']['name']
    character=data['data']['character']['name']
    return quote,anime_name,character 

def movie_quotes():
    url = 'https://quoteapi.pythonanywhere.com/quotes/'
    resp = requests.get(url)

    if resp.status_code == 200:
        data = resp.json()
        quote_list = data["Quotes"][0]
        quote_select = random.choice(quote_list)
        quote = quote_select["quote"]
        movie_title = quote_select["movie_title"]
        actor_name = quote_select["actor_name"]
        return quote,movie_title,actor_name
    else:
        quotes= [
             "In the middle of every difficulty lies opportunity. — Albert Einstein",
            "Happiness depends upon ourselves. — Aristotle",
            "Do what you can, with what you have, where you are. — Theodore Roosevelt",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. — Winston Churchill",
            "Everything you can imagine is real. — Pablo Picasso",
            "Act as if what you do makes a difference. It does. — William James",
            "Don’t count the days, make the days count. — Muhammad Ali",
            "Fall seven times and stand up eight. — Japanese Proverb",
            "Turn your wounds into wisdom. — Oprah Winfrey",
            "It always seems impossible until it’s done. — Nelson Mandela"
        ] 
        return random.choices(quotes)

def nature_quote():
    url = 'https://zenquotes.io/api/quotes/'
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        quote = random.choice(data)
        return quote["q"],quote["a"]
    
        
    else:
        quotes= [
             "In the middle of every difficulty lies opportunity. — Albert Einstein",
            "Happiness depends upon ourselves. — Aristotle",
            "Do what you can, with what you have, where you are. — Theodore Roosevelt",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. — Winston Churchill",
            "Everything you can imagine is real. — Pablo Picasso",
            "Act as if what you do makes a difference. It does. — William James",
            "Don’t count the days, make the days count. — Muhammad Ali",
            "Fall seven times and stand up eight. — Japanese Proverb",
            "Turn your wounds into wisdom. — Oprah Winfrey",
            "It always seems impossible until it’s done. — Nelson Mandela"
        ] 