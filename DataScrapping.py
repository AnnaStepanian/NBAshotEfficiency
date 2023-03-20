import requests
from urllib.parse import urlencode
import json
import pandas

params = {
    'goal_points': {
        'CloseDefDistRange': '',
        'College': '',
        'Conference': '',
        'Country': '',
        'DateFrom': '',
        'DateTo': '',
        'Division': '',
        'DraftPick': '',
        'DraftYear': '',
        'DribbleRange': '',
        'GameScope': '',
        'GameSegment': '',
        'GeneralRange': 'Overall',
        'Height': '',
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': '',
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'PerGame',
        'Period': '0',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': '2021-22',
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'ShotClockRange': '',
        'StarterBench': '',
        'TeamID': '0',
        'TouchTimeRange': '',
        'VsConference': '',
        'VsDivision': '',
        'Weight': ''
    },
    'shooting': {
        'College': '',
        'Conference': '',
        'Country': '',
        'DateFrom': '',
        'DateTo': '',
        'DistanceRange': 'By Zone',
        'Division': '',
        'DraftPick': '',
        'DraftYear': '',
        'GameScope': '',
        'GameSegment': '',
        'Height': '',
        'LastNGames': '0',
        'Location': '',
        'MeasureType': 'Base',
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'PaceAdjust': 'N',
        'PerMode': 'PerGame',
        'Period': '0',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'PlusMinus': 'N',
        'Rank': 'N',
        'Season': '2021-22',
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'ShotClockRange': '',
        'StarterBench': '',
        'TeamID': '0',
        'VsConference': '',
        'VsDivision': '',
        'Weight': '',
    },
    'defense': {
        'College': '',
        'Conference': '',
        'Country': '',
        'DateFrom': '',
        'DateTo': '',
        'DefenseCategory': 'Overall',
        'Division': '',
        'DraftPick': '',
        'DraftYear': '',
        'GameSegment': '',
        'Height': '',
        'LastNGames': '0',
        'LeagueID': '00',
        'Location': '',
        'Month': '0',
        'OpponentTeamID': '0',
        'Outcome': '',
        'PORound': '0',
        'PerMode': 'PerGame',
        'Period': '0',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'Season': '2021-22',
        'SeasonSegment': '',
        'SeasonType': 'Regular Season',
        'StarterBench': '',
        'TeamID': '0',
        'VsConference': '',
        'VsDivision': '',
        'Weight': '',
    }
}


def getDatas(title, param):
    global url
    if title == 'goal_points':
        url = f"https://stats.nba.com/stats/leaguedashplayerptshot?{urlencode(param)}"
    elif title == 'shooting':
        url = f"https://stats.nba.com/stats/leaguedashplayershotlocations?{urlencode(param)}"
    elif title == 'defense':
        url = f"https://stats.nba.com/stats/leaguedashptdefend?{urlencode(param)}"
    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.nba.com',
        'Referer': 'https://www.nba.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    if type(data['resultSets']) is dict:
        pd = pandas.DataFrame(data['resultSets']['rowSet'],
                              columns=list(filter(lambda x: x['name'] == 'columns', data['resultSets']['headers']))[0][
                                  'columnNames'])
    else:
        pd = pandas.DataFrame(data['resultSets'][0]['rowSet'], columns=data['resultSets'][0]['headers'])
    pd.to_csv("Data/" + title + ".csv",  index=False)


for attribute, value in params.items():
    getDatas(attribute, value)
