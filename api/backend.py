import json
import requests
from bs4 import BeautifulSoup as bs
import os
import re

# Main, endless loop

    # Every 10 executions, pull from ESPN API (Regular update condition)

    # Every execution, check page visit statistics.
    # If page visits have increased by 1000% from the average of the previous three minutes, pull from ESPN API (Spike condition)


    # Sleep for 1 minute.

# If the program pulled from the ESPN MLB News API
   # For each article pulled from the API
        # For each shortlisted player
        # If an article uses the name of a shortlisted player in its headline and that article is not in the list of read articles:
            # Download the article
            # Feed the article to ChatGPT, alongside a prompt asking whether the article confirms that the player has signed with any team.

            # Process ChatGPT's response. 
            # If ChatGPT says yes, ask ChatGPT to which team the player has signed.
            # Based on ChatGPT's response, update the page to include the team to which a player has signed besides that player's name.
            # Remove the player's name from the shortlist

        # Add the article to the list of read articles, so it will not be parsed again.

def queryChatGPT(player, articleLink):
    print(player, articleLink)
    return "New York Mets"

def updatePlayer(player, newTeam):
    base=os.path.dirname(os.path.abspath("../html/index.html"))
    html=open(os.path.join(base, "../html/index.html"))
    soup=bs(html, "../html/index.html")


updatePlayer("ohtani", "Toronto Blue Jays")

def pullNews(watchedPlayers):
    espnAPIText = ""
    for i in range(3):
        espnAPIText = requests.get("https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/news")
        if espnAPIText.status_code == 200:
            break
        if i == 2:
            return

    espnAPIDict = espnAPIText.json()

    for article in espnAPIDict["articles"]:
        for player in watchedPlayers:
            if player in article["description"]:
                newTeam = queryChatGPT(player, article["links"]["api"]["news"]["href"])
                
                if newTeam != "":
                    updatePlayer(player, newTeam)

# pullNews(["Chourio"])