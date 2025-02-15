# 2024-11-25.002
import re
import itertools
import telebot
from config import botkey

DEFAULT_START_PORT = 0
DEFAULT_END_PORT = 65535


def group_consecutive_numbers(numbers):
    """Группирует последовательные числа в диапазоны."""
    for _, group in itertools.groupby(enumerate(numbers), key=lambda pair: pair[1] - pair[0]):
        group_list = list(group)
        start = group_list[0][1]
        end = group_list[-1][1]
        yield start, end


def parse_ports_range(input_string):
    """Парсит строку в набор номеров, представляющих диапазон портов."""
    if not input_string:
        return set(range(DEFAULT_START_PORT, DEFAULT_END_PORT + 1))
    try:
        start, end = input_string.split('-')
        if not start.isdigit() or not end.isdigit():
            raise ValueError("Начальный порт и конечный порт должны быть числами.")
        start = int(start)
        end = int(end)
        if start < DEFAULT_START_PORT:
            raise ValueError(f"Начальный порт должен быть больше {DEFAULT_START_PORT}.")
        if end > DEFAULT_END_PORT:
            raise ValueError(f"Конечный порт должен быть меньше {DEFAULT_END_PORT}.")
        if start >= end:
            raise ValueError("Начальный порт должен быть меньше конечного порта.")
    except ValueError as e:
        raise ValueError("Некорректный ввод. Вводите диапазон портов в формате '1-10500'.") from e

    return set(range(start, end + 1))


def parse_cut_ports(input_string):
    """Парсит строку в набор номеров портов для исключения."""
    parts = re.split(r'[ ,]+', input_string)
    ports = set()
    for part in parts:
        match = re.match(r'(\d+)-(\d+)', part)
        if match:
            first = int(match.group(1))
            last = int(match.group(2))
            if first > last:
                raise ValueError("Начальный порт в диапазоне не может быть больше конечного порта.")
            ports.update(range(first, last + 1))
        else:
            if part.isdigit():
                ports.add(int(part))
            else:
                raise ValueError("Некорректный ввод. Допускаются только числа и диапазоны.")
    return ports


# Инициализация бота
bot = telebot.TeleBot(botkey)

# Хранение данных пользователей
user_data = {}


def reset_to_start(chat_id):
    """Сбрасывает состояние пользователя и отправляет сообщение, аналогичное /start."""
    user_data[chat_id] = {'state': None, 'range': None, 'cut_ports': None}
    bot.send_message(
        chat_id,
        "Начнём с начала. Введите команду /range, чтобы установить начальный диапазон портов, "
        "иначе будет использовано значение по умолчанию (0-65535). "
        "Или введите команду /cut для ввода портов для исключения."
    )


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    reset_to_start(message.chat.id)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = (
        "Команды бота:\n"
        "/start - начать всё сначала\n"
        "/help - показать это сообщение\n"
        "/range - установить начальный диапазон портов (в формате '1-10500')\n"
        "/cut - удалить указанные порты или диапазоны из начального диапазона (в формате '1,2-10')\n"
        "На любые другие сообщения бот отвечает 'И чё?'\n"
    )
    bot.send_message(message.chat.id, help_text)


# Обработчик команды /range
@bot.message_handler(commands=['range'])
def handle_range(message):
    user_data[message.chat.id] = {'state': 'waiting_for_range', 'range': None, 'cut_ports': None}
    bot.send_message(
        message.chat.id,
        f"Введите начальный диапазон портов в формате '1-10500' (по-умолчанию {DEFAULT_START_PORT}-{DEFAULT_END_PORT})."
    )


# Обработчик команды /cut
@bot.message_handler(commands=['cut'])
def handle_cut(message):
    if user_data.get(message.chat.id, {}).get('range') is None:
        user_data[message.chat.id]['range'] = set(range(DEFAULT_START_PORT, DEFAULT_END_PORT + 1))
        bot.send_message(message.chat.id, f"Диапазон портов не был задан. Установлено значение по умолчанию: {DEFAULT_START_PORT}-{DEFAULT_END_PORT}.")
    user_data[message.chat.id]['state'] = 'waiting_for_cut_ports'
    bot.send_message(message.chat.id, "Введите номера портов или диапазоны для исключения (в формате '1,2-10'). Разделитель - пробел или запятая. ")


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        user_state = user_data.get(message.chat.id, {}).get('state')

        if user_state == 'waiting_for_range':
            port_range = parse_ports_range(message.text)
            user_data[message.chat.id]['range'] = port_range
            user_data[message.chat.id]['state'] = None
            bot.send_message(message.chat.id, f"Установлен диапазон портов {message.text}. Теперь используйте команду /cut, чтобы исключить порты.")
        elif user_state == 'waiting_for_cut_ports':
            cut_ports = parse_cut_ports(message.text)
            user_data[message.chat.id]['cut_ports'] = cut_ports

            port_range = user_data[message.chat.id]['range']
            result_set = list(port_range - cut_ports)
            grouped_result = ','.join(
                ['%d' % s if s == e else '%d-%d' % (s, e) for (s, e) in group_consecutive_numbers(result_set)]
            )
            user_data[message.chat.id]['state'] = None
            bot.send_message(message.chat.id, f"Результат: {grouped_result}")
        else:
            bot.send_message(message.chat.id, "И чё?")
    except ValueError as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
        reset_to_start(message.chat.id)


# Запуск бота
bot.polling()
