import telebot
from telebot import types
from conf import TOKEN
from db_controller import DataBase

bot = telebot.TeleBot(TOKEN)
db = DataBase(dbname='db/tn-santa.db')

@bot.message_handler(commands=['zapuskator'])
def zapuskator(message):
    db.create_table()
    bot.send_message(message.chat.id,
                     'Спасибо, что запустил меня. Я создал нужную таблицу, заполнил её участниками :)\n'
                     'Если потребуется перезапустить меня, то нужно будет удалить файлы tn-santa.db и tn-santa.db-journal')

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('/list')
    markup.add(button)
    bot.send_message(message.chat.id,
                     'Привет! Я бот, который создаёт пары для тайного санты! Напиши мне /list',
                     reply_markup=markup)

@bot.message_handler(commands=['list'])
def list_message(message):
    bot.send_message(message.chat.id,
                     f'Выбери своё имя! Пожалуйста, пришли мне только номер :) \n\n {db.get_members_list()}')

@bot.message_handler(commands=['db'])
def get_table(message):
    if message.chat.id in [723820184,379167739]:
        bot.send_message(message.chat.id,
                     f'Данные в таблицах: \n\n {db.read_tables()}')
    else:
       bot.send_message(message.chat.id,
                     f'Жулик! Ты не админ!')
    
@bot.message_handler(commands=['santas'])
def santas(message):
    if message.chat.id in [723820184,379167739]:
       bot.send_message(message.chat.id, db.get_santas())
    else:
       bot.send_message(message.chat.id,
                     f'Жулик! Ты не админ!')
    

@bot.message_handler(content_types=['text'])
def func(message):
    if not db.cheque_chat(message.chat.id):
        pair = db.assign_a_couple(player=int(message.text), chat_id=message.chat.id)
        bot.send_message(message.chat.id,
                        f'Ты большой молодец!\nТы будешь тайным сантой для {pair}\n\n'
                        'Пожалуйста, не пиши мне больше ничего\n'
                        'Меня написал одинокий программист пока смотрел мультики и пил пиво \n'
                        'Давай не будем меня ломать, даже если очень хочется :)')
    else:
        bot.send_message(message.chat.id,
                         'Ты уже стал тайным сантой :)')

if __name__ == '__main__':
    bot.polling(non_stop=True)
