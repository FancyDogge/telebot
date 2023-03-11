# импортируем класс родитель
from handlers.handler import Handler

from settings.message import settings


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        обрабатывает входящие /start команды
        """
        self.bot.send_message(message.chat.id,
                              f'{message.from_user.first_name},'
                              f'Здравствуйте! Можно начинать делать покупки.',
                            #   стартовая менюха соответственно, наследуется от Handler, где кейборд и определена
                              reply_markup=self.keybords.start_menu())

    # def pressed_btn_help(self, message):
    #     """
    #     обрабатывает входящие /help команды
    #     """
    #     self.bot.send_message(message.chat.id, settings, parse_mode="HTML", reply_markup=self.keybords.settings_menu())


    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие /start команды. 
        @self.bot.message_handler(commands=['start', 'help'])
        def handle(message):
            # в message много полезного, отлавливаем команду старт и запускаем ф-цию выше
            if message.text == '/start':
                self.pressed_btn_start(message)

            # if message.text == '/help':
            #     self.pressed_btn_help(message)
