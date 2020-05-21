# Простой телеграм бот отвечающий прогнозом погоды @WeatherTelegramBot
# Проверьте не блочится ли API телеграма на уровне провайдера
# Документация https://github.com/eternnoir/pyTelegramBotAPI
#              https://github.com/csparpa/pyowm
# Импортируем пакет с помощью которого мы узнаем погоду

import pyowm

import telebot
import config

# Регистрируемся на сайте погоды, получаем ключ API
owm = pyowm.OWM('d069404c21018306a372846d446e18e3', language='ru')
bot = telebot.TeleBot(config.TOKEN)


# Когда боту пишут текстовое сообщение вызывается эта функция
@bot.message_handler(content_types=['text'])
def send_message(message):
    # Отдельно реагируем на сообщения /start и /help
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
                     parse_mode='html')
    if message.text == "/start":
        bot.send_message(message.from_user.id,
                         "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n")
    elif message.text == "/Start":
        bot.send_message(message.from_user.id,
                         "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n")
    elif message.text == "/Help":
        bot.send_message(message.from_user.id,
                         "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n")
    else:
        # С помощью try заставляю пройти код, если функция observation не находит город
        # и выводит ошибку, то происходит переход к except
        try:
            # Имя города пользователь вводит в чат, после этого мы его передаем в функцию
            observation = owm.weather_at_place(message.text)
            w = observation.get_weather()
            # Присваиваем переменной значение температуры из таблицы
            temp = w.get_temperature('celsius')["temp"]

            # Формируем и выводим ответ
            answer = "В городе " + message.text + " сейчас " + w.get_detailed_status() + \
                "." + "\n"
            answer += "Температура около: " + str(temp) + " С" + "\n\n"
            if temp < -10:
                answer += "Пи**ц как холодно, одевайся как танк!"
            elif temp < 10:
                answer += "Холодно, одевайся теплее."
            elif temp > 25:
                answer += "Жарень."
            else:
                answer += "На улице вроде норм.!!!"
        except:
            answer = "Не найден город, попробуйте ввести название снова.\n"
            # Ответить сообщением
        bot.send_message(message.chat.id, answer)


# Запускаем бота
bot.polling(none_stop=True)
