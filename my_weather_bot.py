from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from weather_config import TOKEN
from weather_models import Gallary
import random
import requests

api_url = "http://api.openweathermap.org/data/2.5/weather"
params = {'q': None, "appid": "11c0d3dc6093f7442898ee49d2430d20", 'units': 'metric'}

bot = TeleBot(TOKEN)


@bot.message_handler(commands = ['start'])
def hello(message):
    kb = ReplyKeyboardMarkup(resize_keyboard = True)
    button = KeyboardButton(text = '/start')
    kb.add(button)
    bot.send_message(message.chat.id, "Hi, I'm a weather forecaster.\nPlease enter city which you want to know "
                                      "weather about.", reply_markup = kb)


@bot.message_handler(content_types = ['text'])
def weather(message):
    params['q'] = message.text.strip()
    res = requests.get(api_url, params = params)
    data = res.json()
    try:
        if data['clouds']['all'] < 40 :
            image = Gallary.get_weather_img('Sunny_weather.jpg')
            res = image.image.read()
            bot.send_photo(chat_id = message.chat.id, photo = res)
        elif data['clouds']['all'] >=40 and data['clouds']['all'] <= 70 :
            image =Gallary.get_weather_img('partial_clouds.jpg')
            res = image.image.read()
            bot.send_photo(chat_id = message.chat.id, photo = res)
        elif data['clouds']['all'] >70:
            choices = ['Thunder_clouds.jpeg', 'Thunder_storm.jpg']
            image = Gallary.get_weather_img(random.choice(choices))
            res = image.image.read()
            bot.send_photo(chat_id = message.chat.id, photo = res)

        bot.send_message(message.chat.id, f"Temperature in {data ['name']} is {round(data ['main'] ['temp'], 1)} °C\n"
                                          f"Feels like {round(data ['main'] ['feels_like'], 1)} °C\n"
                                          f"Pressure {data ['main'] ['pressure']} mbar\n"
                                          f"Humidity {data ['main'] ['humidity']} %\n"
                                          f"Wind speed {data ['wind'] ['speed']} km/h\n"
                                          f"Clouds {data ['clouds'] ['all']} % ")
    except KeyError:
        bot.send_message(message.chat.id, 'Sorry you\'re input invalid city name :(\n'
                                          'Come again ?')


bot.polling()
