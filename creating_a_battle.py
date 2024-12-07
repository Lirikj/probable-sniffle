import time 
from telebot import types 
from config import bot, Channel
from baza import get_random_user, get_user



def creating_battle(message, creathor_id):
    user_id = get_random_user()
    full_name, photo, username = get_user(user_id) 
    creathor_full_name, creathor_photo, creathor_username = get_user(creathor_id)

    message_caption = (f'{creathor_full_name} vs {full_name}')

    question = f"{message_caption} \nИтоги через 4 часа", 
    options = [creathor_full_name, full_name]
    close_time = int(time.time()) + 14400

    media = [
        types.InputMediaPhoto(photo),  
        types.InputMediaPhoto(creathor_photo)]
    
    bot.send_media_group(Channel, media)

    bot.send_poll(
        Channel, 
        question, 
        options, 
        close_date=close_time, )
    
    bot.send_message(creathor_id, '✅Баттл создан')



def creathing_go_battle(message, creathor_id): 
        photo_id = message.photo[-1].file_id  
        file_info = bot.get_file(photo_id)
        file_path = file_info.file_path
        photo = f'https://api.telegram.org/file/bot{bot.token}/{file_path}' 

        bot.send_message(message.chat.id, 'фото я получил, теперь отправь имя')
        bot.register_next_step_handler(message, generation_battle, photo, creathor_id) 


def generation_battle(message, photo, creathor_id):
    full_name = message.text 
    creathor_full_name, creathor_photo, creathor_username = get_user(creathor_id)

    message_caption = (f'{creathor_full_name} vs {full_name}')

    question = f"{message_caption} \nИтоги через 4 часа", 
    options = [creathor_full_name, full_name]
    close_time = int(time.time()) + 14400

    media = [
        types.InputMediaPhoto(photo),  
        types.InputMediaPhoto(creathor_photo)]
    
    bot.send_media_group(Channel, media)

    bot.send_poll(
        Channel, 
        question, 
        options, 
        close_date=close_time, )
    
    bot.send_message(creathor_id, '✅Баттл создан')

