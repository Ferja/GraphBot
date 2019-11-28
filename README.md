# GraphBot

GraphBot is a Telegram bot that textually and graphically (with maps) answer to questions related to geometric graphs defined on  about three million towns throughout the Earth.
The geometric graphs are defined with two different variables `p` and `d`. The graphs will have the towns with population `>=p` as vertexs and the edges will be between towns with distance `<= d`. 

### Prerequisites

In order to execute the bot, you will have to install python in your computer (if you didn't have it installed already). 

```
$ sudo apt-get update
$ sudo apt-get install python3.6
```

### Installing

Create a virtual environment and install the dependencies of the `requirements.txt` file, in order to run the project.

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
Once the dependencies are intalled, we can run the bot with:

```bash
$ python ./graphbot.py
```
If we have internet, we can try the bot in [here](https://t.me/ferran_graph_bot)

## Using the bot
In order to use the bot properly, the user may send their location to build the initial geometric graph.

The commands known by the bot are:

- `/start`

    Initializes the bot. A graph is created with `d`=300 and `p`=100000.

- `/help`

    The bot sends a list with all the possible commands and a brief explanation about their use.

- `/author`

    The bot writes its author information.

- `/graph ⟨distance⟩ ⟨population⟩`

    The bot creates a graph with `d = distance` and `p = population` and uses it from now on.

- `/nodes`

    Writes the number of nodes of the current graph.

- `/edges`

    Writes the number of edges of the current graph.

- `/components`

    Writes the number of connex components of the current graph.

- `/plotpop ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]`

    Plots a map with all the towns on the graph with distance lesser or equal to `dist` from `⟨lat⟩,⟨lon⟩`. The `⟨lat⟩,⟨lon⟩` coordinates are optional, if not given, the bot will take user's location.

- `/plotgraph ⟨dist⟩ [⟨lat⟩ ⟨lon⟩]`

    Plots a map with all the towns on the graph with distance lesser or equal to `dist` from `⟨lat⟩,⟨lon⟩` and their edges. The `⟨lat⟩,⟨lon⟩` coordinates are optional, if not given, the bot will take user's location.

- `/route ⟨src⟩ ⟨dst⟩`

    Plots a map with the shortest path between cities `⟨src⟩` and `⟨dst⟩`.

    The format of the cities is `"Name_of_the_city, country_code"`. An example would be `/route "Barcelona, es" "Zurich, ch"`.

##Libraries used

* [Telegram Bot API](https://core.telegram.org/bots) - API for developing Telegram bots.
* [NetworkX](https://networkx.github.io/) - Python Library used for graph manipulation. 
* [StaticMap](https://github.com/komoot/staticmap) - Python library used for map plotting.
* [Pandas](https://pandas.pydata.org/) - Python library for file managing.
* [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) - Python library for calculating similarity between strings.
* [haversine](https://pypi.org/project/haversine/) - Python library for calculating distances between coordinates.


