import json
import requests
from bs4 import BeautifulSoup as bs
import os
import re
import time
from openai import OpenAI
from dotenv import load_dotenv


def queryChatGPT(player, articleLink):
    articleText = ""
    

    prompt = "Yes or no: does the following text describe either that " + player + " has announced a definitive agreement to join a team, or that a team has announced a definitive agreement to sign " + player + "? Respond \"No\" if the news of the agreement is not from the team or player themselves, but rather from sources outside of the player or team.\n\n" + articleText
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", prompt : prompt}])
    # print(response["choices"][0]["message"]["content"])
    
    print(player, articleLink)
    return "New York Mets"

def updatePlayerStatusInFiles(player, newTeam):
    base=os.path.dirname(os.path.abspath("../html/index.html"))
    html=open(os.path.join(base, "index.html"))

    soup=bs(html, "html.parser")

    old_text=soup.find('h4', {'id':(player + 'Status')})
    new_text=old_text.find(text=re.compile("Unsigned")).replace_with(newTeam)

    with open("../html/index.html", "wb") as f_output:
        f_output.write(soup.prettify("utf-8"))
    
    with open("watchedPlayers.json", "r+") as playersFile:
        players = json.load(playersFile)

        for i in range(len(players)):
            if players[i] == player:
                del players[i]
                break
                
        playersFile.seek(0)
        playersFile.truncate()
        json.dump(players, playersFile)    

def pullNews(watchedPlayers):
    espnAPIText = ""
    for i in range(3):
        espnAPIText = requests.get("https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/news")
        if espnAPIText.status_code == 200:
            break
        if i == 2:
            print("Error: Status code is", espnAPIText.status_code)
            return

    espnAPIDict = espnAPIText.json()

    for article in espnAPIDict["articles"]:
        for player in watchedPlayers:
            if player in article["description"]:
                print("There's news on " + player + "!")
                newTeam = queryChatGPT(player, article["links"]["api"]["news"]["href"])
                
                if newTeam != "":
                    print(player + " is joining " + newTeam + "!")
                    updatePlayerStatusInFiles(player, newTeam)

"""while (True):
    watchedPlayersFile = open("./watchedPlayers.json", "r")
    watchedPlayers = json.load(watchedPlayersFile)[
    watchedPlayersFile.close()

    pullNews(watchedPlayers)

    time.sleep(60)"""

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
print("Hello")
response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content" : "What were the primary causes of the American Revolution?"}])
print(type(response))
print(response.choices[0].message.content)