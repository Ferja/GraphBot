import graphs
import networkx as nx
from telegram.ext import Updater
from telegram.ext import CommandHandler
global_graph = nx.Graph()


# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text="Hola! Soc GraphBot")
    # crea graf inicial
    bot.send_message(chat_id=update.message.chat_id, text="Generant graf inicial...")
    global_graph = graphs.create_graph(300, 100000)
    bot.send_message(chat_id=update.message.chat_id, text="Graf generat!")


def graph(bot, update, args):
    global global_graph
    if len(args) == 2:
        try:
            distance = float(args[0])
            population = float(args[1])
            bot.send_message(chat_id=update.message.chat_id, text="Generant graf...")
            global_graph = graphs.create_graph(distance, population)
            bot.send_message(chat_id=update.message.chat_id, text="Graf generat!")
        except Exception as e:
            print(e)
            bot.send_message(chat_id=update.message.chat_id, text='Hi ha hagut algun error al crear el graf')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Recorda que el format de la comanda /graph és /graph <distance> <population>')


def nodes(bot, update):
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text=str(global_graph.number_of_nodes()))


def edges(bot, update):
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text=str(global_graph.number_of_edges()))


def components(bot, update):
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text=str(global_graph.number_connected_components))


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('graph', graph))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', edges))

# engega el bot
updater.start_polling()
