import telebot
import requests
import json
import settings

bot = telebot.TeleBot(settings.TG_TOKEN)
API = settings.API

dict_of_weather = {
"Clear": "Ясно \U00002600",
"Clouds": "Облачно \U00002601",
"Rain": "Дождь \U00002614",
"Drizzle": "Дождь \U00002614",
"Thunderstorm": "Гроза \U000026A1",
"Snow": "Снег \U0001F328",
"Mist": "Туман \U0001F32B"
}

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    surname = message.from_user.last_name
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, рад тебя видеть!😁 Напиши название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = round(data["main"]["temp"])
        #feels_like = round(data["main"]["feels_like"]) , ощущается как {feels_like} °C
        weather = data["weather"][0]["main"]
        if weather in dict_of_weather:
            wd = dict_of_weather[weather]
        else:
            wd = "Погода не определена"
        bot.reply_to(message, f'Сейчас погода: {temp} °C, {wd}')

        #image = 'sun-color-icon.png' if temp > 5.0 else 'weather-icon.png'
        #file = open('./' + image, 'rb')
        #bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан неверно')

bot.polling(none_stop=True)