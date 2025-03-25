def usersExists(id):
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT EXISTS(SELECT * FROM Users where id = {id});""")
        res = cur.fetchone()
        return bool(res[0])

def AddReward(id, reward):
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        cur.execute(f"""
        UPDATE Users SET invited = invited + {reward} WHERE id = {id};""")

def getRegBy(id):
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT reg_by FROM Users WHERE id = {id};""")
        res = cur.fetchone()
    if res[0] is None:
        return -1
    return res[0]

def regUser(msg, reg_by):
    # Получаем данные
    id = msg.from_user.id
    print(id)
    first_name = msg.from_user.first_name
    username = msg.from_user.username
    last_name = msg.from_user.last_name
    language_code = msg.from_user.language_code

    # Записываем человека
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        print(f"""
        INSERT INTO Users (id, reg_by, first_name, username, last_name, language_code)
        VALUES ({id}, {reg_by}, {first_name}, {username}, {last_name}, {language_code});""")
        cur.execute(f"""
        INSERT INTO Users (id, reg_by, first_name, username, last_name, language_code)
        VALUES ({id}, '{reg_by}', '{first_name}', '{username}', '{last_name}', '{language_code}');""")
        con.commit()
    reward = 1
    req_regBy = reg_by #Переменная для обхода всех юзеров в цепочке
    for i in range(3):
        if usersExists(req_regBy):
            AddReward(req_regBy, reward)
            print(f"Значение у пользователя {req_regBy}, увеличено на {reward}")
            req_regBy =  getRegBy(req_regBy)
        else:
            print("Мы дошли до начала цепочки")
            break

def getUserData(id):
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Users WHERE id = {id};")
        print(f"SELECT * FROM Users WHERE id = {id};")
        res = cur.fetchone()
    return res

def getUserDataName(username):
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        print(f"SELECT * FROM Users WHERE username = '{username.strip('@')}';")
        cur.execute(f"SELECT * FROM Users WHERE username = '{username.strip('@')}';")
        res = cur.fetchone()
    return res

def sendMenu(msg):
    data = getUserData(msg.chat.id)
    print(data)
    inv = data[2]
    trip = data[3]
    ref_url = f"https://t.me/reftest57bot?start={msg.from_user.id}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text = "Обновить", callback_data = "update"))
    markup.add(types.InlineKeyboardButton(text = "Купить трипваер", callback_data="buyTR"))
    markup.add(types.InlineKeyboardButton(text = "Получить трипваер", callback_data = "getTR"))
    text = f"""
    Кол-во приглашенных: {inv}
    Трипваер: {["❌", "✅"][int(bool(trip))]}
    Реферальная ссылка: {ref_url}
    """
    bot.send_message(msg.chat.id, text, reply_markup = markup)

def updateMenu(msg):
    data = getUserData(msg.chat.id)
    print(data)
    inv = data[2]
    trip = data[3]
    ref_url = f"https://t.me/reftest57bot?start={msg.chat.id}"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text = "Обновить", callback_data = "update"))
    markup.add(types.InlineKeyboardButton(text = "Купить трипваер", callback_data="buyTR"))
    markup.add(types.InlineKeyboardButton(text = "Получить трипваер", callback_data = "getTR"))

    text = f"""
    Кол-во приглашенных: {inv}
    Трипваер: {["❌", "✅"][int(bool(trip))]}
    Реферальная ссылка: {ref_url}
    """
    try:
        bot.edit_message_text(text, msg.chat.id, msg.message_id, reply_markup = markup)
    except:
        pass

def getTrip(msg):
    data = getUserData(msg.chat.id)
    print(data)

    if data[2] > 10 or data[3] == 1:
        with open("trip.jpg", "rb") as img:
            bot.send_photo(msg.chat.id, img)

        with sqlite3.connect('data.db') as con:
            cur = con.cursor()
            cur.execute(f"""
            UPDATE Users SET tripvaers = 1 WHERE id = {msg.chat.id};""")
            con.commit()
        bot.send_message(msg.chat.id, "Трипваер успешно приобретен")
        sendMenu(msg)
    else:
        bot.send_message(msg.chat.id, "У вас не хватает приглашений")
    print(data)

def getDataAdmin():
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT username FROM Users ORDER BY invited DESC LIMIT 3;")
        res1 = cur.fetchall()
        cur.execute(f"SELECT count(*) FROM Users;")
        res2 = cur.fetchone()
    return res1, res2

def sendAdminMenu(msg):

    data = getDataAdmin()
    topUsers = []
    for user in data[0]:
        topUsers.append(user[0])
    l = data[1][0]
    markup = types.ReplyKeyboardMarkup()
    markup.add("🔍Найти человека")
    markup.add("💬Рассылка")
    markup.add("🔄Обновить")

    text = f"""
Всего зарегистрировано {l} пользователей
Вот топ 3:\n"""
    for i,v in enumerate(topUsers):
        text += f"{i+1}. {v}\n"
    bot.send_message(msg.chat.id, text, reply_markup = markup)

def sendDataAboutUser(msg, data):
    if data is None:
        bot.send_message(msg.chat.id, "Такой человек не зарегестрирован")
        sendAdminMenu(msg)
        return

    text = ""
    text += f"Id: {data[0]}\n"
    text += f"Приглашен: {data[1]}\n"
    text += f"Кол-во приглашений: {data[2]}\n"
    text += f"Трипваер: {['❌', '✅'][int(bool(data[3]))]}\n"
    text += f"Имя: {data[4]}\n"
    text += f"Никнейм: {data[5]}\n"
    text += f"Фамилия: {data[6]}\n"
    text += f"Страна: {data[7]}\n"

    markup = types.ReplyKeyboardMarkup()
    markup.add("💬Написать")
    markup.add("📄Выдать трипваер")
    markup.add("🔙Назад")
    bot.send_message(msg.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, nextStepFindInf, int(data[0]))

def getListIds():
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT id FROM Users;")
        res = cur.fetchall()
    return list(map(lambda x: x[0], res))
import sqlite3
import telebot
from telebot import types
import configparser
import time

# Чтение конфига
config = configparser.ConfigParser()  # создаём объекта парсера
config.read('config.ini')
TOKEN = config['Telegram']['token']
admin = int(config['Telegram']['adminID'])

# Подготовка бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(msg):
    print(type(msg.chat.id))
    if msg.chat.id == admin:
        sendAdminMenu(msg)
    else:
        text = msg.text.split()

        # Если есть информация
        if len(text) == 2:

            # Это число?
            if text[1].isdigit():
                # Пользователь уже зарегестрирован?
                if usersExists(msg.from_user.id):
                    bot.send_message(msg.chat.id,"Ошибка! Вы уже регистрировались по реферальной программе")
                    sendMenu(msg)
                else:
                    bot.send_message(msg.chat.id, "Здравствуйте")
                    regUser(msg, int(text[1]))
                    bot.send_message(msg.chat.id, "Вы успешно зарегистрировались")
                    sendMenu(msg)
            else:
                regUser(msg, -1)
                sendMenu(msg)
        else:
            if usersExists(msg.from_user.id):
                sendMenu(msg)
            else:
                regUser(msg, -1)
                sendMenu(msg)



@bot.message_handler(content_types=['text'], func=lambda msg: msg.text == "🔍Найти человека")
def findPeople(msg):
    bot.send_message(msg.chat.id, text = "Введите id или его никнейм")
    bot.register_next_step_handler(msg, getIDForFind)

def getIDForFind(msg):
    if len(msg.text):
        if msg.text[0] == "@":
            data = getUserDataName(msg.text)
            sendDataAboutUser(msg, data)

        elif msg.text.isdigit():
            data = getUserData(msg.text)
            sendDataAboutUser(msg, data)

        else:
            sendAdminMenu(msg)

    else:
        sendAdminMenu(msg)

def nextStepFindInf(msg, id):
    if msg.text == "💬Написать":
        bot.send_message(msg.chat.id, "Введите сообщение:")
        bot.register_next_step_handler(msg, sendMessageToUser, id)
    elif msg.text =="📄Выдать трипваер":
        with open("trip.jpg", "rb") as img:
            bot.send_photo(msg.chat.id, img)

        with sqlite3.connect('data.db') as con:
            cur = con.cursor()
            cur.execute(f"""
            UPDATE Users SET tripvaers = 1 WHERE id = {msg.chat.id};""")
            con.commit()
        bot.send_message(msg.chat.id, "Трипваер успешно выдан")
        bot.send_message(id, "Администратор выдал вам трипваер")

    else:
        sendAdminMenu(msg)

def sendMessageToUser(msg, id):
    print("dfsnjjnkl")
    try:
        bot.send_message(id, f"Сообщение от организатора{msg.text}")
    except:
        bot.send_message(msg.chat.id, "Произошла ошибка")
        sendAdminMenu(msg)
    else:
        bot.send_message(msg.chat.id, "Сообщение успешно отправлено")
        sendAdminMenu(msg)

@bot.message_handler(content_types=['text'], func=lambda msg: msg.text == "💬Рассылка")
def updateAdminMenu(msg):
    bot.send_message(msg.chat.id, "Введите текст для рассылки: ")
    bot.register_next_step_handler(msg, mailingGetText)

def mailingGetText(msg):
    users = getListIds()
    for user in users:
        try:
            print(user)
            bot.send_message(user, msg.text)
        except:
            bot.send_message(msg.chat.id, f"Не удалось отправить сообщение пользователю: {user}")
    bot.send_message(msg.chat.id, "Рассылка завершена")
    sendAdminMenu(msg)


@bot.message_handler(content_types=['text'], func=lambda msg: msg.text == "🔄Обновить")
def updateAdminMenu(msg):
    sendAdminMenu(msg)


@bot.callback_query_handler(func=lambda call: True)
def checkCallBack(call):
    if call.data == "update":
        updateMenu(call.message)
    if call.data == "getTR":
        getTrip(call.message)
    if call.data == "buyTR":
        with open("qr.jpg", "rb") as img:
            bot.send_photo(call.message.chat.id, img)
        with open("payments.txt", encoding="UTF-8") as f:
            bot.send_message(call.message.chat.id, f.read())
with sqlite3.connect('data.db') as con:
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    reg_by INTEGER,
    invited INTEGER DEFAULT 0,
    tripvaers INTEGER DEFAULT 0,
    first_name TEXT,
    username TEXT,
    last_name TEXT,
    language_code TEXT)
    """)
    con.commit()


while True:
    try:
        bot.polling(none_stop=True)
    except:
        pass
    else:
        time.sleep(1)
