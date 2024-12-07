from config import bot 
from telebot import types
from creating_a_battle import creating_battle, creathing_go_battle
from telebot.types import LabeledPrice, ShippingOption



random_battle = [LabeledPrice(label="XTR", amount=2)]  
go_battle = [LabeledPrice(label="XTR", amount=15)]  

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 50)),]



def pay_to_random_battle(message):
    bot.send_invoice(
            chat_id=message.chat.id,
            title="photo Battle",
            description="Баттл с рандомным пользователем из нашей базы данных ",
            invoice_payload="Battle",
            provider_token=None, 
            currency="XTR",
            prices=random_battle,
            start_parameter="premium-payment",
        )


def pay_to_go_battle(message):
    bot.send_invoice(
            chat_id=message.chat.id,
            title="photo Battle",
            description="Баттл с предложенным вами пользователем",
            invoice_payload="Battle",
            provider_token=None, 
            currency="XTR",
            prices=go_battle,
            start_parameter="premium-payment",
        )


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Попробуйте еще раз позже')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Попытайтесь заплатить еще раз через несколько минут, нам нужен небольшой отдых")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id

    if payload == 'random_battle':
        bot.send_message(message.chat.id,
                        'Ищем пользователя для баттла'.format(
                            message.successful_payment.total_amount / 100, message.successful_payment.currency),
                        parse_mode='Markdown') 
        creating_battle(message, user_id)

    elif payload == 'go_battle':
        bot.send_message(message.chat.id,
                        'Пришлите фото пользователя для баттла'.format(
                            message.successful_payment.total_amount / 100, message.successful_payment.currency),
                        parse_mode='Markdown') 
        bot.register_next_step_handler(message, creathing_go_battle, user_id)
