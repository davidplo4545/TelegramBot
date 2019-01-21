import matplotlib.pyplot as plt
import telegram
import os


IMAGE_PATH = 'image.jpg'


def generate_graph(bot, chat_id, stock_data, symbol):
    '''
    generates a graph for the stock and sends
    through telegram
    :param bot:
    :param chat_id:
    :param stock_data:
    :param symbol:
    :return:
    '''
    x_values = [item[0]for item in stock_data]
    y_values = [float(item[1])for item in stock_data]

    plt.clf()

    # set graph settings
    plt.title('Ticker symbol:' + symbol)
    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.plot(x_values, y_values, 'o-', markersize=1)
    plt.xticks([x_values[i] for i in range(len(x_values)) if i % 52 == 0])

    # check if image exists, remove it is
    if os.path.isfile(IMAGE_PATH):
        os.remove(IMAGE_PATH)

    plt.savefig(IMAGE_PATH)
    bot.send_photo(chat_id=chat_id, photo=open(IMAGE_PATH, 'rb'))


