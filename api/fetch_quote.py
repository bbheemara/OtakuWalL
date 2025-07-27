import requests  



def quotes():
    url='https://api.animechan.io/v1/quotes/random'
    resp=requests.get(url)
    data=resp.json()
    quote=data['data']['content']
    anime_name=data['data']['anime']['name']
    character=data['data']['character']['name']
    return quote,anime_name,character 
