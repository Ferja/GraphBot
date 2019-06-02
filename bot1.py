import graphs
import maps
import networkx as nx
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

global global_graph, user_lat, user_lon


# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    print('bot started')
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text="Hola! Soc GraphBot")
    # crea graf inicial
    bot.send_message(chat_id=update.message.chat_id, text="Generant graf inicial...")
    global_graph = graphs.create_graph(300, 100000)
    bot.send_message(chat_id=update.message.chat_id, text="Graf generat!")


def where(bot, update, user_data):
    print('received location')
    global user_lat, user_lon
    try:
        user_lat, user_lon = update.message.location.latitude, update.message.location.longitude
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


def graph(bot, update, args):
    print('received graph')
    global global_graph
    try:
        if len(args) == 2:
            distance = float(args[0])
            population = float(args[1])
            bot.send_message(chat_id=update.message.chat_id, text="Generant graf...")
            global_graph = graphs.create_graph(distance, population)
            bot.send_message(chat_id=update.message.chat_id, text="Graf generat!")
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Recorda que el format de la comanda /graph és /graph <distance> <population>')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='Hi ha hagut algun error al crear el graf')


def nodes(bot, update):
    print('received nodes')
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text=str(global_graph.number_of_nodes()))


def edges(bot, update):
    print('received edges')
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text=str(global_graph.number_of_edges()))


def components(bot, update):
    print('received components')
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text=str(nx.number_connected_components(global_graph)))


def plotpop(bot, update, args):
    global global_graph, user_lat, user_lon
    print('received plotpop')
    try:
        if len(args) == 3 or len(args) == 1:
            dist = float(args[0])
            if len(args) == 3:
                lat = float(args[1])
                lon = float(args[2])
            elif len(args) == 1:
                lat = user_lat
                lon = user_lon
            bot.send_message(chat_id=update.message.chat_id, text="Generant plot...")
            fitxer = maps.draw_map_plotpop(global_graph, dist, lat, lon)
            bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
            os.remove(fitxer)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Recorda que el format de la comanda /plotpop és /plotpop <dist> [<lat> <lon>]')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hi ha hagut algun error al crear el plot, torna-ho a intentar')


def plotgraph(bot, update, args):
    global global_graph, user_lat, user_lon
    print('received plotgraph')
    try:
        if len(args) == 3 or len(args) == 1:
            dist = float(args[0])
            if len(args) == 3:
                lat = float(args[1])
                lon = float(args[2])
            elif len(args) == 1:
                lat = user_lat
                lon = user_lon
            bot.send_message(chat_id=update.message.chat_id, text="Generant plot...")
            fitxer = maps.draw_map_plotgraph(global_graph, dist, lat, lon)
            bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
            os.remove(fitxer)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Recorda que el format de la comanda /plotgraph és /plotgraph <dist> [<lat> <lon>]')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hi ha hagut algun error al crear el plot, torna-ho a intentar')


def route(bot, update, args):
    global global_graph
    print('received route')
    try:
        if len(args) == 2:
            src = args[0]
            dst = args[1]
            bot.send_message(chat_id=update.message.chat_id, text="Generant plot...")
            fitxer = maps.draw_map_route(global_graph, src, dst)
            bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
            os.remove(fitxer)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Recorda que el format de la comanda /route és /route <src> <dst>')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hi ha hagut algun error al crear el plot, torna-ho a intentar')


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# handlers
dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args=True))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', components))
dispatcher.add_handler(CommandHandler('plotpop', plotpop, pass_args=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_args=True))
dispatcher.add_handler(CommandHandler('route', route, pass_args=True))

# engega el bot
updater.start_polling()
