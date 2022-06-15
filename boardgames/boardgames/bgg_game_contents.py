from bs4 import BeautifulSoup
import requests
import sqlite3
import lxml
import time
import pandas as pd
import json
import os


def get_contents(id):
    # try:
    r = requests.get(
        f"https://boardgamegeek.com/xmlapi2/thing?id={id}?comments=1&stats=1",
        headers={'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"})

    if r.status_code == 429:
        time.sleep(int(r.headers['Retry-After']))
        # r.raise_for_status()
    # except requests.exceptions.HTTPError as err:
    #    print('Requests Exception found.')
    #    raise err

    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find('name', {'type': 'primary'})['value']

    # game Thumbnail
    thumbnail = ''
    try:
        thumbnail = soup.find('thumbnail').text
    except:
        thumbnail = 'https://cf.geekdo-images.com/micro/img/QZDNfKAPYlXkZg265NxdjgShBXY=/fit-in/64x64/pic1657689.jpg'

    # suggested_numPlayers
    # votes
    # id 3 : Best
    # id 2 : Recommended
    # id 1 : Not Recommended
    suggested_numPlayers = {}

    # language dependence levels
    # level 0 : No votes
    # level 1 : No necessary in-game text
    # level 2 : Some necessary text - easily memorized or small crib sheet
    # level 3 : Moderate in-game text - needs crib sheet or paste ups
    # level 4 : Extensive use of text - massive conversion needed to be playable
    # level 5 : Unplayable in another language
    language_Dependence = {0: 0}
    polls = soup.findAll('poll')

    for poll in polls:
        if poll['name'] == 'suggested_numplayers' and int(poll['totalvotes']) != 0:
            numplayers = poll.findAll('results')
            for numplayer in numplayers:
                votes = numplayer.findAll('result')
                suggested_numPlayers[numplayer['numplayers']] = {
                    1: int(votes[2]['numvotes']),  # Not Recommended
                    2: int(votes[1]['numvotes']),  # Recommended
                    3: int(votes[0]['numvotes'])}  # Best
        if poll['name'] == 'language_dependence' and int(poll['totalvotes']) != 0:
            dependences = poll.findAll('result')
            for dependence in dependences:
                language_Dependence[int(dependence['level'])] = int(
                    dependence['numvotes'])

    # Best , Recommended, NotRecommended Players
    playersRecommended = []
    playersBest = []
    playersNotRecommended = []

    for num in suggested_numPlayers:
        values = list(suggested_numPlayers[num].values())
        keys = list(suggested_numPlayers[num].keys())
        maxVotes = keys[values.index(max(values))]

        if maxVotes == 1:
            playersNotRecommended.append(num)
        elif maxVotes == 2:
            playersRecommended.append(num)
        else:
            playersBest.append(num)

    # Num Players
    minPlayer = soup.find('minplayers')['value']
    maxPlayer = soup.find('maxplayers')['value']

    minPlayerRecommended = 0
    maxPlayerRecommended = 0
    try:
        minPlayerRecommended = max(minPlayer, min(playersRecommended))
        maxPlayerRecommended = min(maxPlayer, max(playersRecommended))
    except:
        minPlayerRecommended = 0
        maxPlayerRecommended = 0

    print("Min Player Recommended: ", minPlayerRecommended)
    print("Max Player Recommended: ", maxPlayerRecommended)
    players = [playersBest, playersRecommended, playersNotRecommended]

    keys = list(language_Dependence.keys())
    values = list(language_Dependence.values())

    # suggested Language Dependence
    suggested_language_Dependence = keys[values.index(max(values))]

    # Playing Time
    minPlayTime = soup.find('minplaytime')['value']
    maxPlayTime = soup.find('maxplaytime')['value']

    # Min Age
    minAge = soup.find('minage')['value']

    # game category, mechanic, family, expansion, designer, artist, publisher
    boardgameCategory = []
    boardgameMechanic = []
    boardgameDesigner = []
    boardgameFamily = []
    boardgameExpansion = []
    boardgameArtist = []
    boardgamePublisher = []

    for eachtag in soup.findAll('link'):
        if eachtag['type'] == 'boardgamecategory':
            boardgameCategory.append(eachtag['id'])
        elif eachtag['type'] == 'boardgamemechanic':
            boardgameMechanic.append(eachtag['id'])
        elif eachtag['type'] == 'boardgamedesigner':
            boardgameDesigner.append(eachtag['id'])
        elif eachtag['type'] == 'boardgamefamily':
            boardgameFamily.append(eachtag['id'])
        elif eachtag['type'] == 'boardgameexpansion':
            try:
                if eachtag['inbound'] == 'true':
                    inbound = True
            except:
                inbound = False
            boardgameExpansion.append(
                {'id': eachtag['id'], 'inbound': inbound})
        elif eachtag['type'] == 'boardgameArtist':
            boardgameArtist.append(eachtag['id'])
        elif eachtag['type'] == 'boardgamePublisher':
            boardgamePublisher.append(eachtag['id'])

    # group ranks
    # { subgroup name : { rank : bayesaverage } }
    ranks = {}
    for ranking in soup.findAll('rank'):
        ranks[ranking['name']] = {
            ranking['value'] if ranking['value'].isnumeric() else 'N/A':
            ranking['bayesaverage'] if not ranking['bayesaverage'] == 'Not Ranked' else 'N/A'}

    # statistics
    usersrated = soup.find('usersrated')['value']
    average = soup.find('average')['value']
    bayesaverage = soup.find('bayesaverage')['value']
    stddev = soup.find('stddev')['value']
    median = soup.find('median')['value']
    owned = soup.find('owned')['value']
    wishing = soup.find('wishing')['value']

    # weights
    numcomments = soup.find('numcomments')['value']
    print("Num Comments: ", numcomments)
    numweights = soup.find('numweights')['value']
    averageweight = soup.find('averageweight')['value']

    contents = [{'id': id,
                'title': title,
                 'thumbnail': thumbnail,
                 'language_dependence': suggested_language_Dependence,
                 'players': players,
                 'playersBest': playersBest,
                 'minPlayer': minPlayer,
                 'maxPlayer': maxPlayer,
                 'minPlayerRecommended': minPlayerRecommended,
                 'maxPlayerRecommended': maxPlayerRecommended,
                 'minPlayTime': minPlayTime,
                 'maxPlayTime': maxPlayTime,
                 'minAge': minAge,
                 'usersrated': usersrated,
                 'average': average,
                 'bayesaverage': bayesaverage,
                 'stddev': stddev,
                 'median': median,
                 'owned': owned,
                 'wishing': wishing,
                 'numcomments': numcomments,
                 'numweights': numweights,
                 'averageweight': averageweight,
                 'ranks': ranks,
                 'boardgamecategory': boardgameCategory,
                 'boardgamemechanic': boardgameMechanic,
                 'boardgameexpansion': boardgameExpansion,
                 }]

    return contents


pwd = os.getcwd()
con = sqlite3.connect(pwd+'/boardgames.db')
df = pd.read_sql_query('SELECT * FROM games LIMIT 30;', con)

# get all contents & db insert
start_time = time.time()
print(start_time)
results = []
for index, row in df.iterrows():
    try:
        contents = get_contents(row['id'])
        print('Language dependence: ', contents[0]['language_dependence'])
        print('Avg. weight: ', contents[0]['averageweight'])
        results.append(contents)
    except:
        print("Houston we have a problem!!! ", row['id'])

    time.sleep(2)

with open('results.json', 'w') as f:
    json.dump(results, f)
print(time.time() - start_time)
