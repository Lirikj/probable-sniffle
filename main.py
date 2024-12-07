from telebot import types 
from config import bot 
from pay import pay_to_random_battle, pay_to_go_battle
from baza import init_db, check_user_exists, get_user, add_user


@bot.message_handler(commands=['start'])
def menu_message(message):
    user = message.from_user
    user_id = message.from_user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name if user.last_name else ''

    if check_user_exists(user_id):
        markup = types.InlineKeyboardMarkup()
        go_battle = types.InlineKeyboardButton('👊Батл', callback_data='go_battle')
        random_battle = types.InlineKeyboardButton('🔀Рандомный батл', callback_data='random_battle')
        markup.add(go_battle)
        markup.add(random_battle)

        full_name, photo, username_baza = get_user(user_id)
        bot.send_photo(message.chat.id, photo, caption=f"📖Твоя анкета \n \n{full_name}", reply_markup=markup) 
    else: 
        bot.send_message(message.chat.id, f'👋Привет, {first_name} {last_name}!'
                        '\n'
                        '\nЯ 🤖@NurlatphotoBattlebot, я устраиваю фото батлы')
        bot.send_message(message.chat.id, 'Давай для начала зарегистрируем тебя в системе'
                        '\n'
                        '\nОтправь мне фото, которое хочешь использовать в батлах') 
        bot.register_next_step_handler(message, user_registration)



def user_registration(message):
    try:
        if message.content_type == 'photo':
            user = message.from_user
            user_id = message.from_user.id
            username = user.username
            first_name = user.first_name
            last_name = user.last_name if user.last_name else ''

            photo_id = message.photo[-1].file_id  
            file_info = bot.get_file(photo_id)
            file_path = file_info.file_path
            photo = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'

            add_user(user_id, username, first_name, last_name, photo)
            bot.send_message(message.chat.id, '😁Ура, ты зарегистрирован')
            menu_message(message)

        else:
            bot.send_message(message.chat.id, "мне нужно, чтоб вы отправили фото, попробуйте еще раз")
            bot.register_next_step_handler(message, user_registration) 
    except Exception as e:
        print(e)



@bot.callback_query_handler(func=lambda callback: callback.data in ['go_battle', 'random_battle'])
def buttons(callback):
    if callback.data == 'random_battle':
        pay_to_random_battle(callback.message)
    elif callback.data == 'go_battle':
        pay_to_go_battle(callback.message)



init_db()
bot.polling(none_stop=True)

