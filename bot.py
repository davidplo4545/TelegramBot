import requests
import json
import matplotlib.pyplot as plt
import telegram

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from graph import generate_graph
from stock import Stock
from maplestory import get_latest_posts
from global_time import get_world_timezone

API_KEY = 'TELEGRAM_API_KEY_HERE'


class TelegramBot:
    def __init__(self):
        self.token = API_KEY
        self.updater = Updater(self.token)
        self.dp = self.updater.dispatcher
        self.setup_handlers()
        self.base = 'https://api.telegram.org/bot{}'.format(self.token)

    def setup_handlers(self):
        '''
        Adds the handlers to the dispatcher
        :return:
        '''
        self.dp.add_handler(CommandHandler('stock', self.send_daily_data, pass_args=True))
        self.dp.add_handler(CommandHandler('graph', self.send_stock_graph, pass_args=True))
        self.dp.add_handler(CommandHandler('time', self.send_timezone, pass_args=True))
        self.dp.add_handler(CommandHandler('maple', self.send_latest_posts))
        # self.dp.add_handler(CommandHandler('start', self.start))

    def run(self):
        print('The bot is now running...')
        self.updater.start_polling()

    def send_message(self, bot, update, text):
        # send message to the bot
        bot.send_message(chat_id=update.message.chat_id, text=text,parse_mode=telegram.ParseMode.MARKDOWN)

    def send_stock_graph(self, bot, update, args):
        symbol = ''.join(args)
        print('Requested graph: {}'.format(symbol))
        try:
            stock = Stock(symbol)
            generate_graph(bot, update.message.chat_id, stock.get_historical_data(), symbol.upper())
            print('Graph sent successfully.')
        except Exception as e:
            self.send_message(bot, update, 'error')
            print('Error occured retrieving data:{}'.format(symbol))

    def send_daily_data(self, bot, update, args):
        symbol = ''.join(args)
        print('Requested Data: {}'.format(symbol))
        try:
            stock = Stock(symbol)
            daily_data = stock.get_daily_data()
            self.send_message(bot, update, daily_data)
            print('Retrieved Data: {}'.format(symbol))
        except Exception as e:
            print(e)
            self.send_message(bot, update, 'error')
            print('Error occured retrieving data:{}'.format(symbol))

    def send_latest_posts(self, bot, update):
        latest_posts = get_latest_posts()
        response = ''

        for post in latest_posts:
            # some formatting
            # make bold
            title = '*' + post[0] + '*'
            # set it as link
            link = '(' + post[1] + ')'
            response += '[Click here]'.join([title +'\n', link + '\n'])

        self.send_message(bot, update, response)

    def send_timezone(self, bot, update, args):
        try:
            msg = get_world_timezone(''.join(args))
            self.send_message(bot, update, msg)
        except Exception as e:
            print('Error occured retrieving data:{}'.format(symbol))


    def start(self, bot, update):
        '''
        Just a test function to check a different
        type of keyboard
        :param bot:
        :param update:
        :return:
        '''
        # txt = 'Hey! I am Stockman, a Bot for stocks <> \n send \\help to know more!'
        # self.send_message(bot, update, txt)
        button_list = [
            telegram.InlineKeyboardButton("col1", callback_data='nothing'),
            telegram.InlineKeyboardButton("col2",callback_data='nothing'),
            telegram.InlineKeyboardButton("row 2",callback_data='nothing')
        ]
        try:
            reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        except Exception as e:
            print(e)

        try:
            bot.send_message(update.message.chat_id,"A two-column menu", reply_markup=reply_markup)
        except Exception as e:
            print(e)

# just an example function from the web
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu






