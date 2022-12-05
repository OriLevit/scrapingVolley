from urllib.request import urlopen
import soup_manager
from tqdm import tqdm

league_table = urlopen('https://www.iva.org.il/boards.asp')

all_leagues_links = soup_manager.get_leagues(league_table)
all_teams = []
all_games = []

for link in tqdm(all_leagues_links, bar_format='{l_bar}{bar:100}', desc="Gathering teams", leave=False, disable=False):
    league_title = soup_manager.get_title(urlopen(link))
    soup_manager.get_teams(urlopen(link), all_teams)
    league_games = []
    soup_manager.get_upcoming_games(urlopen(link), league_games)
    soup_manager.get_upcoming_games(urlopen(link), all_games)
    soup_manager.print_games(league_games,league_title)


