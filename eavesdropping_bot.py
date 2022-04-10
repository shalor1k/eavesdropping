import telebot
from telebot import types
import re
import datetime
import os
import time as tm

chats = []
added_chats = []
filename = 'messages.txt'
time = os.path.getmtime(filename)

bot = telebot.TeleBot('API HASH')

keywords_list = []
name_delete = ""
string = ''


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start' or message.text == 'Вернуться в начало' or message.text == 'Стоп':
        global keywords_list
        keywords_list = []
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))

        msg = bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=start_keyboard)

        bot.register_next_step_handler(msg, query_handler)


def query_handler(message):
    if message.text == 'Ввести ключевые слова':
        keywords_keyboard = types.ReplyKeyboardMarkup()
        keywords_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))
        msg = bot.send_message(message.chat.id, 'Введите ключевые слова через запятую, в формате (слово1, слово2)',
                               reply_markup=keywords_keyboard)

        bot.register_next_step_handler(msg, keywords_or_restart)

    elif message.text == 'Настройка чатов':

        settings_keyboard = types.ReplyKeyboardMarkup()
        settings_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))
        settings_keyboard.add(types.KeyboardButton(text='Добавить чат'))
        settings_keyboard.add(types.KeyboardButton(text='Удалить чат'))

        second_string = ''
        if len(added_chats) != 0:
            for i in added_chats:
                second_string += i + '\n'

        msg = bot.send_message(message.chat.id, 'Вот список чатов для парсинга:\n' + second_string,
                               reply_markup=settings_keyboard)
        bot.register_next_step_handler(msg, settings)


def keywords_or_restart(message):
    if message.text == 'Вернуться в начало':

        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))

        msg = bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=start_keyboard)
        bot.register_next_step_handler(msg, query_handler)

    else:
        keywords = str(message.text)
        keywords_list = keywords.split(',')
        print(keywords_list)
        f = open('keywords.txt', 'w')
        f.close()

        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text="Да"))
        markup.add(types.KeyboardButton(text="Нет"))

        msg = bot.send_message(message.chat.id, 'Запускаем парсинг по ключевым словам: ' + keywords
                               + '\nВсё указано верно?', reply_markup=markup)
        bot.register_next_step_handler(msg, apply)


def apply(message):
    if message.text == 'Нет':
        msg = bot.send_message(message.chat.id, 'Возвращаемся к вводу ключевых слов')
        global keywords_list
        keywords_list = []
        bot.register_next_step_handler(msg, keywords_or_restart)

    else:
        settings_keyboard = types.ReplyKeyboardMarkup()
        settings_keyboard.add(types.KeyboardButton(text='Стоп'))
        msg = bot.send_message(message.chat.id, 'Парсинг запущен успешно', reply_markup=settings_keyboard)
        bot.register_next_step_handler(msg, parsing)


def settings(message):
    if message.text == 'Вернуться в начало':
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))

        msg = bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=start_keyboard)
        bot.register_next_step_handler(msg, query_handler)

    elif message.text == 'Добавить чат':
        settings_keyboard = types.ReplyKeyboardMarkup()
        settings_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))

        msg = bot.send_message(message.chat.id, 'Проверьте, что чат уже добавлен в аккаунт-парсер и вы получаете' +
                               ' от него сообщения, а затем введите сюда имя на данный чат',
                               reply_markup=settings_keyboard)

        bot.register_next_step_handler(msg, add_chat)

    else:
        settings_keyboard = types.ReplyKeyboardMarkup()
        settings_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))

        msg = bot.send_message(message.chat.id, 'Введите имя чата, который хотите удалить из парсинга',
                               reply_markup=settings_keyboard)

        bot.register_next_step_handler(msg, remove_chat)


def add_chat(message):
    if message.text == 'Вернуться в начало':
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))

        msg = bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=start_keyboard)
        bot.register_next_step_handler(msg, query_handler)

    elif 'Уверен' in message.text:
        name = message.text[40:]
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))
        second_string = '\n'
        for i in added_chats:
            second_string += i + '\n'
        msg = bot.send_message(message.chat.id, 'Чат добавлен, вот список добавленных чатов\nДобавите ещё парочку?'
                               + second_string, reply_markup=start_keyboard)
        bot.register_next_step_handler(msg, add_chat)

    else:
        name = message.text

        if name in chats:
            start_keyboard = types.ReplyKeyboardMarkup()
            start_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))
            second_string = '\n'
            for i in added_chats:
                second_string += i + '\n'
            msg = bot.send_message(message.chat.id, 'Чат добавлен, вот список добавленных чатов\nДобавите ещё парочку?'
                                   + second_string, reply_markup=start_keyboard)
            bot.register_next_step_handler(msg, add_chat)
        else:
            settings_keyboard = types.ReplyKeyboardMarkup()
            settings_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))
            settings_keyboard.add(types.KeyboardButton(text='Уверен, что следующий чат есть в чатах: ' + str(name)))
            msg = bot.send_message(message.chat.id, 'Чат не найден на аккаунте-парсере,'
                                                    ' попробуйте ввести название заново, или если вы уверены,'
                                                    ' что чат есть, нажмите на кнопку', reply_markup=settings_keyboard)
            bot.register_next_step_handler(msg, add_chat)


def remove_chat(message):
    if message.text == 'Вернуться в начало':
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))

        msg = bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=start_keyboard)
        bot.register_next_step_handler(msg, query_handler)

    else:
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text="Да"))
        markup.add(types.KeyboardButton(text="Нет"))
        markup.add(types.KeyboardButton(text="Вернуться в начало"))
        global name_delete
        name_delete = str(message.text)
        msg = bot.send_message(message.chat.id, 'Вы уверены, что хотите удалить следующий чат из парсинга?\n'
                               + name_delete, reply_markup=markup)
        bot.register_next_step_handler(msg, remove_chat_next_step)


def remove_chat_next_step(message):
    if message.text == 'Вернуться в начало':
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))

        msg = bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=start_keyboard)
        bot.register_next_step_handler(msg, query_handler)

    elif message.text == "Нет":
        settings_keyboard = types.ReplyKeyboardMarkup()
        settings_keyboard.add(types.KeyboardButton(text='Вернуться в начало'))

        msg = bot.send_message(message.chat.id, 'Введите имя чата, который хотите удалить из парсинга',
                               reply_markup=settings_keyboard)

        bot.register_next_step_handler(msg, remove_chat)

    elif message.text == 'Да':

        pattern = re.compile(re.escape(name_delete))

        second_string = '\n'
        added_chats.remove(name_delete)
        if len(added_chats) != 0:
            for i in added_chats:
                second_string += i + '\n'
        msg = bot.send_message(message.chat.id, 'Чат успешно удалён.\nВот список чатов для парсинга:\n' + second_string)


def parsing(message):
    if message.text == "Вернуться в начало":
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))
        msg = bot.send_message(message.chat.id, "Парсинг отменён, наступило время моего законного отдыха, если что,"
                                                " обращайтесь", reply_markup=start_keyboard)
        bot.register_next_step_handler(msg, query_handler)

    elif message.text == 'Стоп':
        start_keyboard = types.ReplyKeyboardMarkup()
        start_keyboard.add(types.KeyboardButton(text='Ввести ключевые слова'))
        start_keyboard.add(types.KeyboardButton(text='Настройка чатов'))

        msg = bot.send_message(message.chat.id, 'И снова здравствуйте', reply_markup=start_keyboard)

        bot.register_next_step_handler(msg, query_handler)
    else:
        global time
        print(1)
        while True:
            print(2)
            if os.path.getmtime(filename) > time:
                start_keyboard = types.ReplyKeyboardMarkup()
                start_keyboard.add(types.KeyboardButton(text='Стоп'))
                print(3)
                time = os.path.getmtime(filename)
                f = open("messages.txt", 'r', encoding='utf-8')
                for line in f:
                    bot.send_message(message.chat.id, line, reply_markup=start_keyboard)
                f = open('messages.txt', 'w')
                f.close()


bot.polling(none_stop=True, interval=0)
