from datetime import datetime
import requests
import pymongo

API_KEY = '61051d147f304411804184153221506'
location = 'Moscow'
URL = 'http://api.weatherapi.com/v1/current.json?key=' + API_KEY + '&q=' + location + '&aqi=yes'
 

def get_weather(URL):
    while True:
        client = pymongo.MongoClient("mongodb://localhost:27017") #or ("localhost", 27017)

        # connect or create  DB
        db = client["waetherDB"]

        # collection (if not exist -> create)
        collection = db["weather"]  
    
        r = requests.get(URL)
        jason_whater = r.json()

        data_input = int(input('Посмотреть погоду сейчас - 1\nПосмотреть всю БД - 2\nЗавершить программу - 3\n'))
        if data_input == 1: 
            try:
                print('\nТемпература - ' + str(jason_whater['current']['temp_c']))
                print('Скорость ветра - ' + str(jason_whater['current']['wind_kph']) + '\n')
                
                data = {  
                    'temp': str(jason_whater['current']['temp_c']),
                    'wind speed': str(jason_whater['current']['wind_kph']),
                    'timezone': str(jason_whater['location']['tz_id']),
                    'time': str(datetime.now())         
                }
                # if collection.find().sort("temp", -1).limit(1) == data.get('temp'):
                   
            except:
                data={
                    'name': 'ERROR',
                    'tiem': str(datetime.now())
                }
                collection.insert_one(data)
                print('Не удалось найти погоду.')  
        elif data_input == 2:
            for i in collection.find():
                try:
                    print('температура - ' + str(i.get('temp')))
                    print('скорость ветра - ' + str(i.get('wind speed')))
                    print('времаная зона - ' + str(i.get('timezone')))
                    print('время - ' + str(i.get('time'))+'\n')

                except:
                    print(i.get('name'))
                    print('cтатус - ' + i.get('cod'))
                    print('время - ' + i.get('time')+'\n')
                    print(' ')
        elif data_input == 3:
            break
        elif data_input == 96:
            client.drop_database('waetherDB')
get_weather(URL) 
    