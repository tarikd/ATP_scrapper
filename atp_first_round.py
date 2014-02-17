# coding: utf-8

from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys
import os
import shutil

sys.setrecursionlimit(30000)

mon_fichier = open("fichier.txt", "w")

# Fonction qui renvoie le html parsé
def make_soup(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

# Fonction qui récupère le nom du tournoi
def get_tournament_title(soup):
    title = soup.find("a", "tournamentTitle").string
    return title

# Fonction qui récupère le lieu du tournoi
def get_tournament_location(soup):
    location = soup.find("p", "tournamentSubTitle").string.split(" -")[0]
    return location

# Fonction qui récupère la date de début et de fin du tournoi
def get_tournament_date(soup):
    date = soup.find("p", "tournamentSubTitle").string.split("- ")[1]
    debut = date.split("-")[0].encode('utf-8')
    fin = date.split("-")[1].encode('utf-8')
    return debut, fin

# Fonction qui récupère le type de surface
def get_tournament_surface(soup):
    inlineWrapper = soup.find("span", "inlineWrapper")
    surface = inlineWrapper.findAll("p")[1]
    surface = str(surface).split(">")[3]
    surface = surface.split("<")[0]
    return surface

# Fonction qui récupère la dotation du tournoi
def get_tournament_prizemoney(soup):
    inlineWrapper = soup.find("span", "inlineWrapper")
    prizemoney = inlineWrapper.findAll("p")[2]
    prizemoney = str(prizemoney).split(">")[3]
    prizemoney = prizemoney.split("<")[0]
    return prizemoney

# Fonction qui récupère le nom et prénom de tous les joueurs du premier tour
def get_player_name_first_round(soup):
    colonne1 = soup.find("td", "col_1")
    playerWrap = colonne1.findAll("div", "playerWrap")
    list_player_first_round = []
    for name in playerWrap:
        list_player_first_round.append(name.a.string)
    return list_player_first_round

######################################################################################################

# Fonction qui récupère le nom et prénom de tous les gagnants du premier tour
def get_player_name_first_round_winner(soup):
    colonne2 = soup.find("td", "col_2")
    playerWrap = colonne2.findAll("div", "playerWrap")
    list_winner_first_round = []
    for name in playerWrap:
        list_winner_first_round.append(name.a.string)
    return list_winner_first_round


# Fonction qui récupère le score du match du premier tour
def get_player_score_first_round_winner(soup):
    colonne2 = soup.find("td", "col_2")
    scores = colonne2.findAll("div", "scores")
    list_score_first_round = []
    for score in scores:
        list_score_first_round.append(score.a.string)
    return list_score_first_round

##############################################################################################

# URL du drawing pour un tournoi une année précise

URL = "http://www.atpworldtour.com/Share/Event-Draws.aspx?e=540&y=2013"

##############################################################################################

BASE_URL_YEAR = "http://www.atpworldtour.com/Share/Event-Draws.aspx?e=540&y="

BASE_URL_NAME = "http://www.atpworldtour.com/Share/Event-Draws.aspx?e="

rg = 520

tournamentYear_urls = [BASE_URL_YEAR + str(year) for year in range(1996,2014)]

tournamentName_urls = [BASE_URL_NAME + str(rg) + "&y=2012"]

soup = make_soup(URL)

# Création du fichier
mon_fichier = open(get_tournament_title(soup)+"_First_Round", "w")

mon_fichier.write(get_tournament_title(soup)+"\n")
mon_fichier.write(get_tournament_location(soup)+"\n")
mon_fichier.write(str(get_tournament_surface(soup))+"\n")
mon_fichier.write(str(get_tournament_prizemoney(soup))+"\n")
mon_fichier.write(""+"\n")



mon_fichier.write('{ANNEE:<10} {TOUR:<15} {JOUEUR1:<25} {JOUEUR2:<25} {GAGNANT:<25} {SCORE}'.format(ANNEE="ANNEE", TOUR="TOUR", JOUEUR1="JOUEUR1", JOUEUR2="JOUEUR2", GAGNANT="GAGNANT", SCORE="SCORE"))
mon_fichier.write("\n\n")

tournamentYear = 1996

for tournamentYear_url in tournamentYear_urls:
    i = 0
    n = 0
    j = 0
    soup = make_soup(tournamentYear_url)

    while i < len(get_player_name_first_round(soup)):
        winner = get_player_name_first_round_winner(soup)[n]
        score = get_player_score_first_round_winner(soup)[n]
        n+=1
        mon_fichier.write('{tournamentYear:<10} {Round:<15} {Player1:<25} {Player2:<25} {Gagnant:<25} {Score}'.format(tournamentYear=str(tournamentYear), Round=str("First Round"), Player1=get_player_name_first_round(soup)[i], Player2=get_player_name_first_round(soup)[i+1], Gagnant=winner, Score=score))
        mon_fichier.write("\n")        
        i+=2
    tournamentYear+=1


if not os.path.exists("Wimbledon"):
    os.makedirs("Wimbledon")

shutil.move(get_tournament_title(soup)+"_First_Round", "Wimbledon/")




