from urllib.request import urlopen
import soup_manager
from tqdm import tqdm
import helper

LEAGUE_TABLE = urlopen('https://www.iva.org.il/boards.asp')

all_leagues_links = soup_manager.get_leagues(LEAGUE_TABLE)
all_teams = []
all_games = []

for link in tqdm(all_leagues_links, bar_format='{l_bar}{bar:100}', desc="Gathering information", leave=False, disable=False):
    league_title = soup_manager.get_title(urlopen(link))
    soup_manager.get_teams(urlopen(link), all_teams)
    helper.get_games(link, league_title, all_games)
