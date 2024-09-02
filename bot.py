import config
import telebot
from telebot import types # кнопки Telegram

bot = telebot.TeleBot(config.token)


user_num1 = ''
user_num2 = ''
user_proc = ''
user_result = None

#если /start, /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # убрать клавиатуру Telegram полностью
    markup =types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id, "Привет " + message.from_user.first_name + ", я бот-калькулятор\nВведит число", reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)


#Введите первое число
def process_num1_step(message, user_result = None):
    try:
        global user_num1


        # запоминаем число
        #если только начали /start
        if user_result == None:
            user_num1 = int(message.text)
        else:
            # если был передан результат ранее
            # пишем в первое число, не спрашивая
            user_num1 = str(user_result)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('+')
        itembtn2 = types.KeyboardButton('-')
        itembtn3 = types.KeyboardButton('*')
        itembtn4 = types.KeyboardButton('/')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        
        msg = bot.send_message(message.chat.id, "Выбрите операцию", reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc_step)
    except Exception as e: 
        bot.reply_to(message, "Это не число или что то пошло не так")

#выберите операцию +, -, *, /
def process_proc_step(message):
    try:
        global user_proc

        # запоминаем оперцию
        user_proc = message.text
        # убрать клавиатуру Telegram полностью
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(message.chat.id, "Введите еще число", reply_markup=markup)
        bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
        bot.reply_to(message, 'Вы ввели что то другое или что то пошло н так ')

# Введите второе число
def process_num2_step(message):
    try:
        global user_num2

        #запоминаем число
        user_num2 = int(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('Результат')
        itembtn2 = types.KeyboardButton('Продолжить вычисление')
        markup.add(itembtn1, itembtn2)

        msg = bot.send_message(message.chat.id, "Показать результат или продолжить операцию?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
        bot.reply_to(message, 'Это не число или что то пошло не так')

# показать результат или продолжить оперцию
def process_alternative_step(message):
    try:
        #сделать вычисление
        calc()

        # убрать клавиатуру Telegram полностью
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() == 'результат':
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text.lower() == 'продолжить вычисление':
            # перейти на шаг, где спрашиваем оператор
            # передаем результат, как первое число
            process_num1_step(message, user_result)
    
    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так')

#Вывод результата пользователю
def calcResultPrint():
    global user_num1, user_num2, user_proc, user_result
    return "Результат: " + str(user_num1) + " " + user_proc + ' ' +str(user_num2) + ' = ' + str(user_result)

#Вычисление
def calc():
    global user_num1, user_num2, user_proc, user_result

    user_result = eval(str(user_num1) + user_proc + str(user_num2))

    return user_result

#Enable saving next step handLers to file "./.handLers-saves/step.save".abs
#DeLay=2 means that afer any change in next step handlers (e.g. calling register_next_step_handler())
#saving will hapen after dalay 2 seconds
bot.enable_save_next_step_handlers(delay=2)

#Load next_step_handlers from save file (default "./.handlers-saves/step.save")
#Warning It willwork only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)