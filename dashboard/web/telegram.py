from datetime import datetime

import telebot

from web.config import global_config


class Telegram:
    def __init__(self, token):
        self.token = token
        self.bot = None
        self.set_bot(token)

    def set_bot(self, token):
        self.bot = telebot.TeleBot(token)

    def send_detection(self, instance, labels, scores, image):
        for group in instance.groups.all():
            for user in group.user_set.all():
                try:
                    if labels is None:
                        message = "📸Instantanea:\nCámara: {}\nFecha: {}".format(instance.name, datetime.now())
                    else:
                        message = "📸Detección:\nCámara: {}\nFecha: {}\nItems: {}\nProbs%: {}".format(instance.name,
                                                                                                     datetime.now(),
                                                                                                     labels, scores)
                    self.bot.send_message(user.chat_id, message)
                    self.bot.send_photo(user.chat_id, image)
                except:
                    print("Usuario con id: {} no ha iniciado un chat con la app".format(user.chat_id))


telegram_component = Telegram(global_config.get_config("token"))
