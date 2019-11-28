import graphs
import maps
import networkx as nx
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

global global_graph, user_lat, user_lon


def start(bot, update):
    print('bot started')
    global global_graph
    bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm GraphBot")
    # creates initial graph
    bot.send_message(chat_id=update.message.chat_id, text="Generating initial graph...")
    global_graph = graphs.create_graph(300, 100000)
    bot.send_message(chat_id=update.message.chat_id, text="Graph generated!")
    bot.send_message(chat_id=update.message.chat_id, text="You may send me your current location...")


def where(bot, update, user_data):
    print('received location')
    global user_lat, user_lon
    try:
        user_lat, user_lon = update.message.location.latitude, update.message.location.longitude
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


def help(bot, update):
    print('received /help')
    text = open('help.txt').read()
    bot.send_message(chat_id=update.message.chat_id, text=text)


def author(bot, update):
    print('received author')
    bot.send_message(chat_id=update.message.chat_id, text="Ferran Velasco Olivera\nferran.velasco.olivera@est.fib.upc.edu")


def graph(bot, update, args):
    print('received graph')
    global global_graph
    try:
        if len(args) == 2:
            distance = float(args[0])
            population = float(args[1])
            bot.send_message(chat_id=update.message.chat_id, text="Generating graph...")
            global_graph = graphs.create_graph(distance, population)
            bot.send_message(chat_id=update.message.chat_id, text="Graph generated!")
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Remember: the command format is /graph <distance> <population>')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error was encountered while creating the graph')


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
            bot.send_message(chat_id=update.message.chat_id, text="Generating plot...")
            fitxer = maps.draw_map_plotpop(global_graph, dist, lat, lon)
            bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
            os.remove(fitxer)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Remember: the command format is /plotpop <dist> [<lat> <lon>]')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='An error was encountered while creating the plot, please try again')


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
            bot.send_message(chat_id=update.message.chat_id, text="Generating plot...")
            fitxer = maps.draw_map_plotgraph(global_graph, dist, lat, lon)
            bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
            os.remove(fitxer)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Remember: the command format is /plotgraph <dist> [<lat> <lon>]')
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='An error was encountered while creating the plot, please try again')


def route(bot, update, args):
    global global_graph
    print('received route')
    try:
        s = ' '
        srcdst = s.join(args).split('"')
        src = srcdst[1]
        dst = srcdst[3]
        bot.send_message(chat_id=update.message.chat_id, text="Generating plot...")
        fitxer = maps.draw_map_route(global_graph, src, dst)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
        os.remove(fitxer)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id,
                         text='An error was encountered while creating the plot, please try again')


# gets TOKEN from token.txt
TOKEN = open('token.txt').read().strip()

# creates objects to work with telegram
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# handlers
dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('author', author))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args=True))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', components))
dispatcher.add_handler(CommandHandler('plotpop', plotpop, pass_args=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_args=True))
dispatcher.add_handler(CommandHandler('route', route, pass_args=True))

# starts the bot
updater.start_polling()
