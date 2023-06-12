import requests # импортируем библиотеку для отправки запросов
import telebot # импортируем библиотеку для работы с телеграмом
import json # импортируем библиотеку для передачи данных пользователю в читаемом виде

from config import token,api  # из файла config.py забираем нашу переменную с токеном и ключ для API яндекс.погода

bot = telebot.TeleBot(token) # создаем бота с токеном

@bot.message_handler(commands=["start"]) # команда /start
def start(message):
  # отправляем приветственное сообщение с приглашением ввести город
  bot.send_message(message.chat.id,
                   "Привет! Рад видеть! "
                   "В каком городе интересует погодка?")

@bot.message_handler(content_types=['text']) # Будем обрабатывать только текстовые сообщения.Не картинки, не аудио.
def get_weather(message): # Создаем функцию с принимаемым параметром message
  city = message.text.strip() # Информация полученная от пользователя с функией убирающей пробелы
  res =requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')# передаем данные(город) по url адресу

  if res.status_code==200: # 200 успешная обработка url страницы, т.е. город нашелся
   data = json.loads(res.text) #создаем переменную data с помощью которой мы обращаемся к функции loads методa json в которую предатся текст с сайта res.text
   temp = data["main"]["temp"]# Вычленяем с помощью словаря и ключей ["main"]["temp"] показания температуры
   cloud = data["clouds"]["all"]# Вычленяем показания облачности
   wind = data["wind"]["speed"]# Вычленяем показания скорости ветра
   wind_gust = data["wind"]["gust"]# Вычленяем показания скорости ветра при порывах
   humidity = data["main"]["humidity"]# Вычленяем с помощью словаря и ключей ["main"]["humidity"] показания влажности
   bot.send_message(message.chat.id, f'Сейчас температура в городе {city}: {temp} градусов Цельсия.'
                                    f'\n Облачность {cloud} %. '
                                    f'\n Скорость ветра {wind} м/с. При порывах {wind_gust} м/с. '
                                    f'\n Влажность {humidity} %')  #bot.send_message(message.chat.id,f'Сейчас погода:{res.json()}')
   # bot.send_message(message.chat.id,f'Сейчас погода:{res.json()}')
   if 25 <= temp:
      bot.send_message(message.chat.id, f'Одевайтесь легко и не забывайте про солнцезащитный крем.'
                                        f'\n  Важно пить достаточное количество воды!')  # отправляем сообщение пользователю
   elif 25 > temp >= 10:
      bot.send_message(message.chat.id, f'У природы нет плохой погоды ;)')
   elif temp < 10:
      bot.send_message(message.chat.id, f'Одевайтесь потеплее и не простудитесь.')  # отправляем сообщение пользователю

  else:
    bot.send_message(message.chat.id, f'Город указан неверно. Попробуйте ещё раз.')#  в случае неверно введенного города  отправляем сообщение пользователю



bot.polling(none_stop=True)#, interval=0) # запускаем бота