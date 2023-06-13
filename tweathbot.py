import requests
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Замените 'ВАШ_ТОКЕН' на токен доступа вашего бота
TOKEN = 'ВАШ_ТОКЕН'

# Замените 'ВАШ_API_КЛЮЧ' на ваш API-ключ OpenWeatherMap
API_KEY = 'ВАШ_API_КЛЮЧ'


# Обработчик команды /start
def start(update, context):
    command_list = [
        "/weather - получить текущую погоду",
        "/start - показать список команд"
    ]
    reply_text = "Привет! Я бот погоды. Я поддерживаю следующие команды:\n\n" + "\n".join(command_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text)


# Обработчик команды /weather
def weather(update, context):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Получение текущей погоды
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Vladivostok&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    # Извлечение данных о погоде из ответа API
    temperature = response['main']['temp']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']

    # Формирование сообщения о погоде
    message = f"Текущая погода в г. Владивосток: ({current_time}) \nТемпература: {temperature}°C\nВлажность: {humidity}%\nОписание: {description}"

    # Отправка сообщения
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    logging.info(f"Запрос погоды от пользователя {update.effective_user.username} ({current_time})")


# Обработчик текстовых сообщений
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    weather_handler = CommandHandler('weather', weather)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(weather_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
