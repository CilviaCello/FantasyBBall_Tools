from yahoo_oauth import OAuth2
import xml.etree.ElementTree as ET
import csv

# Establishes oauth2 authentication
oauth = OAuth2(None,None,from_file='oauth2.json')
if not oauth.token_is_valid():
    oauth.refresh_access_token()

leagueId = "31821"

"""
# OAuth resource transaction ex.
# Send request for league resource
uri = "https://fantasysports.yahooapis.com/fantasy/v2/team/nba.l." + leagueId
oauth.session.get(uri) # XMLHttpRequest.response
"""

def set_league(newId):
    """
    Parameters:
    newId (int): New league id to use for resource extraction
    """
    global leagueId
    leagueId = newId
    uri = "https://fantasysports.yahooapis.com/fantasy/v2/team/nba.l." + leagueId
    rsrc = oauth.session.get(uri)
    print(rsrc.text)

def get_team(teamId):
    """
    Parameters:
    teamId (int): Key value of team in fantasy league

    Returns:
    XMLHttpRequest.response: Yahoo Fantasy Sports requested team resource
    """
    uri = "https://fantasysports.yahooapis.com/fantasy/v2/team/nba.l." + leagueId + ".t." + str(teamId)
    return oauth.session.get(uri)

def get_team_stats(teamId):
    """
    Parameters:
    teamId (int): Key value of team in fantasy league

    Returns:
    XMLHttpRequest.response: Yahoo Fantasy Sports resource for current week's stats
    """
    uri = "https://fantasysports.yahooapis.com/fantasy/v2/team/nba.l." + leagueId + ".t." + str(teamId) + "/stats;type=week;week=current"
    return oauth.session.get(uri)

def get_roster(teamId):
    """
    Parameters:
    teamId (int): Key value of team in fantasy league

    Returns:
    XMLHttpRequest.response: Yahoo Fantasy Sports requested roster resource (current)
    """
    uri = "https://fantasysports.yahooapis.com/fantasy/v2/team/nba.l." + leagueId + ".t." + str(teamId) + "/roster"
    return oauth.session.get(uri)

def get_player(playerId):
    """
    Parameters:
    playerId (int): Key value of player in fantasy league

    Returns:
    XMLHttpRequest.response: Yahoo Fantasy Sports requested player resource
    """
    uri = "https://fantasysports.yahooapis.com/fantasy/v2/player/nba.p." + str(playerId)
    return oauth.session.get(uri)

def get_transaction(transId):
    """
    Parameters:
    transId (int): Key value of fantasy league transaction

    Returns:
    XMLHttpRequest.response: Yahoo Fantasy Sports requested transaction resource
    """
    uri = "https://fantasysports.yahooapis.com/fantasy/v2/transaction/nba.l." + leagueId + ".tr." + str(transId)
    return oauth.session.get(uri)

def write_stats():
    csvfile = open('fantasy_stat.csv', 'w', newline='')
    fieldnames = ['Team','fgm/fga','fg%','ftm/fta','ft%','3ptm','pts','reb','ast','stl','blk','to']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for x in range(1, 12):
        response = get_team_stats(x)
        if response == False:
            print("Requested resource not found")
            return
        root = ET.fromstring(response.text)[0]

        name = root.find('{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}name').text
        # team stats are stored in a List
        stats = []
        for child in root.iter('{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}stat'):
            val = child.find('{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}value').text
            stats.append(val)
        writer.writerow({'Team':name, 'fgm/fga':stats[0], 'fg%':stats[1], 'ftm/fta':stats[2], 'ft%':stats[3], '3ptm':stats[4], 'pts':stats[5], 'reb':stats[6], 'ast':stats[7], 'stl':stats[8], 'blk':stats[9], 'to':stats[10]})

