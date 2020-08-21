import telebot
import requests
from telebot import types
from config import *


def get_weather(city):
    result = requests.get(url + "q=" + city + "&lang=ru&units=metric&appid=" + api_key).json()
    return result


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def input_city(message):
    keyboard = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "\N{cityscape} Введите город: ", reply_markup=keyboard)
    bot.register_next_step_handler(msg, show_weather)


def show_weather(message):
    try:
        city = message.text
        weather = get_weather(city)

        temp = weather["main"]["temp"]
        feels_like = weather["main"]["feels_like"]
        pressure = weather["main"]["pressure"] / 1.333     # перевод гектопаскалей в мм рт. ст.
        humidity = weather["main"]["humidity"]
        description = weather["weather"][0]["description"]

        bot.send_message(message.chat.id, f"Погода на сегодня:\n"
                                          f"\N{black small square} Температура: {temp:.0f} °С\n"
                                          f"\N{black small square} Ощущается как: {feels_like:.0f} °С\n"
                                          f"\N{black small square} Давление: {pressure:.0f} мм рт. ст.\n"
                                          f"\N{black small square} Влажность: {humidity}%\n"
                                          f"\N{black small square} Описание: {description}")

    except Exception as e:
        bot.send_message(message.chat.id, "Город не найдет!")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
