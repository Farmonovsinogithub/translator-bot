import telebot
from telebot.types import *
import googletrans

translator = googletrans.Translator()

config = "5663157501:AAELIUYnoDMrUdSUdsJomnFuHI_xN883Dww"

bot = telebot.TeleBot(config)

def choose_lang_buttons():
    ibtn1 = InlineKeyboardButton("🇺🇿 O'zbek", callback_data='uzb')
    ibtn2 = InlineKeyboardButton("🇷🇺 Русский", callback_data='rus')
    ibtn3 = InlineKeyboardButton("🇺🇸 English", callback_data='eng')
    btn = InlineKeyboardMarkup(row_width=1).add(ibtn1, ibtn2, ibtn3)
    return btn

@bot.message_handler(commands=['start', "help"])
def start_and_help(message):
    global msg
    msg = bot.send_message(message.chat.id, f" Salom {message.from_user.full_name}\ntilni tanlang\nchoose language\nвыберите язык👇", reply_markup=choose_lang_buttons())

@bot.callback_query_handler(func=lambda call: call.data == 'uzb')
def uzb(call):
    global lang
    lang = 1
    bot.send_message(call.message.chat.id, f"Salom {call.message.from_user.full_name}\nMen tarjimon botman\nmenga so'z yuboring")
    bot.delete_message(chat_id=call.message.chat.id, message_id=msg.id)

@bot.callback_query_handler(func=lambda call: call.data == 'eng')
def eng(call):
    global lang
    lang = 2
    bot.send_message(call.message.chat.id, f"Hello {call.message.from_user.full_name}\nI'm translator bot\nsend me anything word")
    bot.delete_message(chat_id=call.message.chat.id, message_id=msg.id)

@bot.callback_query_handler(func=lambda call: call.data == 'rus')
def eng(call):
    global lang
    lang = 3
    bot.send_message(call.message.chat.id, f"Привет {call.message.from_user.full_name}\nбот для тестирования\nЯ бот-переводчик пришли мне слово")
    bot.delete_message(chat_id=call.message.chat.id, message_id=msg.id)

@bot.message_handler(func=lambda message: True)
def main(message):
    detect = translator.detect(message.text).lang
    if message.text == "mine":
        bot.send_message(message.chat.id, "meniki, shaxta")
    else:
        if detect == "uz":
            bot.send_message(message.chat.id, translator.translate(message.text, dest='en').text)
            bot.send_message(message.chat.id, translator.translate(message.text, dest='ru').text)
        elif detect == "ru":
            bot.send_message(message.chat.id, translator.translate(message.text, dest='uz').text)
            bot.send_message(message.chat.id, translator.translate(message.text, dest='en').text)
        elif detect =='en':
            bot.send_message(message.chat.id, translator.translate(message.text, dest='uz').text)
            bot.send_message(message.chat.id, translator.translate(message.text, dest='ru').text)
        else:
            if lang == 1:
                bot.send_message(message.chat.id, "kechirasiz, men bu so'zni tarjimasini topaolmadim 😔")
            elif lang == 2:
                bot.send_message(message.chat.id, "Sorry, but I couldn't find the translation of this word 😔")
            elif lang == 3:
                bot.send_message(message.chat.id, "извините, я не смог найти перевод этого слова 😔")


bot.infinity_polling(timeout=None, long_polling_timeout=False)