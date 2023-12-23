import json
import requests
from bs4 import BeautifulSoup as bs
import os
import re
import time
from openai import OpenAI
from dotenv import load_dotenv

def cleanupHTML(input):
    output = ""
    outputting = True

    for c in input:
        if c == '<' or c == '>':
            outputting = not outputting
        elif outputting:
            output += c

    output = output.rstrip()

    return output


def queryChatGPT(player, articleLink):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
    articleText = ""

    espnAPIText = ""
    for i in range(3):
        espnAPIText = requests.get(articleLink)
        if espnAPIText.status_code == 200:
            break
        if i == 2:
            print("Error: Status code is", espnAPIText.status_code)
            return "API Error"
        
    
    articleJSON = espnAPIText.json()
    articleText = articleJSON["headlines"][0]["story"]
    articleText = cleanupHTML(articleText)

    #  If so, respond simply with the full name of the team, stylized with the city name and nickname; for example, \"Washington Nationals\" or \"San Francisco Giants,\" with no other text in your response. Otherwise, respond simply with the word \"No.\"\

    myPrompt = "Does the following text say with which team " + player.title() + " will certainly play in the next season? Ignore anything that the text says about any other player; focus solely on " + player.title() +".\n\n" + articleJSON["headlines"][0]["title"]  + "\n" + articleJSON["headlines"][0]["description"] + "\n" + articleText

    # print(myPrompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role":"user", "content" : myPrompt}], temperature=.3)
    # print(response.choices[0].message.content)
    responseText = response.choices[0].message.content

    teamsFile = open("./teams.json", "r")
    teams = json.load(teamsFile)
    teamsFile.close()

    for i in range(len(teams)):
        team = teams[i][0]
        if team in responseText:
            if ("source" not in articleJSON["headlines"][0]["description"].lower()) and ("source" not in articleJSON["headlines"][0]["title"].lower()) and ("rumor" not in articleJSON["headlines"][0]["description"].lower()) and ("rumor" not in articleJSON["headlines"][0]["title"].lower()):
                return team
            else:
                return "No."
        
    return "No."
    
    if (responseText.startswith("No")):
        responseText = ""

    return ""

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

def pullNews(watchedPlayers, readArticles):
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
        if not (article["dataSourceIdentifier"] in readArticles):
            apiError = False


            for player in watchedPlayers:
                if ((player in article["description"].lower()) and (article["premium"] == False) and (article["type"] == "HeadlineNews") and ("source" not in article["description"].lower()) and ("source" not in article["headline"].lower()) and ("rumor" not in article["description"].lower()) and ("rumor" not in article["headline"].lower())):
                    newTeam = queryChatGPT(player, article["links"]["api"]["news"]["href"])
            
                    if newTeam == "API Error":
                        apiError = True
                        break
                    if newTeam != "":
                        updatePlayerStatusInFiles(player, newTeam)
            if apiError == False: 
                with open("./readArticles.json", "r+") as readArticlesFile: 
                    readArticlesJSON = json.load(readArticlesFile)
                    readArticlesJSON.append(article["dataSourceIdentifier"])
                    readArticlesFile.seek(0)
                    readArticlesFile.truncate()
                    json.dump(readArticlesJSON, readArticlesFile)

while (True):
    watchedPlayersFile = open("./watchedPlayers.json", "r")
    watchedPlayers = json.load(watchedPlayersFile)
    watchedPlayersFile.close()

    readArticlesFile = open("./readArticles.json", "r")
    readArticles = json.load(readArticlesFile)
    readArticlesFile.close()

    pullNews(watchedPlayers, readArticles)

    time.sleep(180)