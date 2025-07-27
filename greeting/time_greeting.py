from datetime import datetime

def getCurrentHour():
    current_datetime=datetime.now()
    return current_datetime.hour
message=""
def getMessage():
    hour=getCurrentHour()

    if hour >=0 and hour < 5:
      message="Go Sleep That's Enough for Today 🛏️💤"
      return message


    elif hour < 12:
      message="Morning champ!! ☀️"  
      return message


    elif hour < 18:
       message="Afternoon Remember to eat! 🍜"
       return message


    else:
       message="Evening!! 🌆"   
       return message 

