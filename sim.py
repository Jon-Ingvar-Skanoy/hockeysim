import pickle
import numpy as np

from numba import prange
from scipy.stats import betabinom, nbinom
import random
import copy
import tqdm
import multiprocessing

class Team:
    def __init__(self,name, games_played, goals_for,goals_against,shots_on_goal,shots_against, id):
        self.t = games_played 
        self.k = shots_on_goal
        self.binom_a =goals_against
        self.binom_b = shots_against- self.binom_a
        self.name = name
        self.poisson_la= (self.t*60)/(self.t*60+1)
        self.points = 0
        self.ma = 0
        self.id = id
        self.match_history = []
        self.beaten = []
        
#Antakelse: Det er IKKE høyere sjanse for mål ved "shoutout"
#Antakelse: statistikken vi har inkluderer ikke overtid


def sim_game(team1,team2):
    team1.ma +=1
    team2.ma +=1 # hjelpe variabel for å verifisere velykket kjøring av programmet
    team2.match_history.append(team1.id) # vi lagrer en liste med hvilke lag som har spilt med hvem for å kunne analyserer det i ettertid
    team1.match_history.append(team2.id)
    # her er poisson prediktiv fordelig negative binom fordeling her sumeres opp 60 1 minutt prosseser
    shots_team1 = sum(nbinom.rvs(team1.k,(team1.poisson_la),size=60))
    shots_team2 = sum(nbinom.rvs(team2.k,(team2.poisson_la),size=60))
    # her er en bernoulli prosses sin prediktive fordeling beta binomial fordelig, denne kjøres like mange ganger som poisson prossesen ga. 
    goals_team1 = betabinom.rvs(shots_team1,team2.binom_a,team2.binom_b)
    goals_team2 = betabinom.rvs(shots_team2,team1.binom_a,team1.binom_b)

    if (goals_team1==goals_team2): # hvis uavgjort
        # her er poisson prediktiv fordelig negative binom fordeling her sumeres opp 5 1 minutt prosseser, siden man spiller 5 minutter overtid
        shots_team1 = sum(nbinom.rvs(team1.k,(team1.poisson_la),size=5))
        shots_team2 = sum(nbinom.rvs(team1.k,(team2.poisson_la),size=5))
         # her er en bernoulli prosses sin prediktive fordeling beta binomial fordelig, denne kjøres like mange ganger som poisson prossesen ga. 
        goals_team1 = betabinom.rvs(shots_team1,team2.binom_a,team2.binom_b)
        goals_team2 = betabinom.rvs(shots_team2,team1.binom_a,team1.binom_b)

        if (goals_team1==goals_team2):# hvis uavgjort igjen
            while True:
                # tre skudd mot mål per lag til en vinner er funnet
                goals_team1 = betabinom.rvs(3,team2.binom_a,team2.binom_b) 

                goals_team2 = betabinom.rvs(3,team1.binom_a,team1.binom_b)
                if (goals_team1!=goals_team2):
                    break
        # setter poeng git utvidet tid
        if (goals_team1<goals_team2):
            team1.points +=1
            team2.points +=2
            team2.beaten.append(team1.id)
            return [1,2]
        if (goals_team1>goals_team2):
            team1.points +=2
            team2.points +=1
            team1.beaten.append(team2.id)
            return [2,1]
    # setter poeng gitt avgort i første 60 min
    if (goals_team1<goals_team2):
        team1.points +=0
        team2.points +=2
        team2.beaten.append(team1.id)
        return [0,2]
    if (goals_team1>goals_team2):
        team1.points +=2
        team2.points +=0
        team1.beaten.append(team2.id)
        return [2,0]


def subdivision_simulation(teams):
    # siden lagene skal forsjellige mengder kamper mot hverandre må vi ha en tilfeldig prosess. 
    # det ble vurdert slit at det er enkelst at alle spiller mot sine naboer i listen, derfor må listen være i tilfelig rekefølge som shuffle gjør for oss.
    random.shuffle(teams)
    for i in range(0,8):
        if( i != 7):#denne delingen er grunnet at listen er en liste og ikke en sirkel
            
            sim_game(teams[i],teams[i+1])# spill 3 kamper mot neste mann i listen
            sim_game(teams[i],teams[i+1])
            sim_game(teams[i],teams[i+1])
            for team in teams:
                if (team == teams[i] or team == teams[i+1] or teams[i-1] == team):
                   pass
                else:# spill to kamper mot de andre og når de andre også er her blir det 4 kamper totalt
                    sim_game(team,teams[i])
                    sim_game(team,teams[i])
        else: # samme men tilpasset slik at team[i+1] er erstatted med team[0] 
            sim_game(teams[i],teams[0])
            sim_game(teams[i],teams[0])
            sim_game(teams[i],teams[0])
            for team in teams:
                if (team == teams[i] or team == teams[0] or teams[i-1] == team):
                    pass
                else:
                    sim_game(team,teams[i])
                    sim_game(team,teams[i])
               

def division_simulation(division):
    # hvert team skall spille 3 kamper mot hvert team i annen divisjon
    for team in division[0]:
        for i in range(8):
            sim_game(team, division[1][i])
            sim_game(team, division[1][i])
            sim_game(team, division[1][i])


def interconference_simulation(teams):
    div1 = teams[0]
    div2 = teams[1]
    # hvert team skall spille 2 kamper mot hvert team i annen konforanse
    for subdivision in div1:
        for team in subdivision:
                for subdivision2 in div2:
                    for team2 in subdivision2:
                        sim_game(team,team2)
                        sim_game(team,team2)
  
    
def season_simulation(teams):
    for division in teams:
        for subdivision in division:
            subdivision_simulation(subdivision)
        division_simulation(division)
    interconference_simulation(teams)
    return teams



def season_simulation_wrapper(teams,n):
    outcomes = []
    for i in tqdm.tqdm(range(n)):
        copyteam = copy.deepcopy(teams)
        outcome = season_simulation(copyteam)
        outcomes.append(outcome)
    return outcomes


def create_teams():
    # henter data fra pickle filer
    data = pickle.load(open("20-23.p", "rb"))
    names = pickle.load(open("names_20-23.p", "rb"))
    mTeams = []
    # lager liste strukturen
    aTeams = []
    cTeams = []
    pTeams = []
    eDivision = [mTeams, aTeams]
    wDivision = [cTeams, pTeams]
    teams = [eDivision, wDivision]
    garbagecan = []
    i =0

    # går gjennom hvert lag og setter dem i riktig divisjon
    for row in data:
        
        tmp = Team(names[i],row[0],row[1],row[2],row[3],row[4], id=i)
        # her er inputtet names = navn, # games played = row[0], Goals = row[1], Goals against = row[2], Shots = row[3], Shots against = row[4]
        if(tmp.name in ["Carolina Hurricanes","New Jersey Devils", "New York Rangers","Columbus Blue Jackets", "New York Islanders", "Philadelphia Flyers", "Washington Capitals","Pittsburgh Penguins"]):
            mTeams.append(tmp)
        elif(tmp.name in ["Dallas Stars","Colorado Avalanche","Minnesota Wild", "Winnipeg Jets","Nashville Predators", "St. Louis Blues", "Arizona Coyotes", "Chicago Blackhawks"]):
            cTeams.append(tmp)
        elif(tmp.name in ["Boston Bruins", "Toronto Maple Leafs", "Tampa Bay Lightning", "Florida Panthers", "Buffalo Sabres", "Ottawa Senators", "Detroit Red Wings", "Montreal Canadiens"]):
            aTeams.append(tmp)
        elif(tmp.name in ["Vegas Golden Knights","Edmonton Oilers", "Calgary Flames","Vancouver Canucks","Los Angeles Kings", "San Jose Sharks","Anaheim Ducks","Seattle Kraken"]):
            pTeams.append(tmp)
        else:
            garbagecan.append(tmp)
        i +=1
    # her sender vi lagene til en pickle fil, slik at sansynlighetsfordelinger kan plottes.
    pickle.dump(teams, open("teams_in_div.p", "wb"))
    return teams


if __name__ == '__main__':
    teams = create_teams()
    n = 1000
    m = 6
    input = []
    pool = multiprocessing.Pool(processes=m)
    for i in prange(m):
        input.append((teams, n))
    results = pool.starmap(season_simulation_wrapper,input)
    resultArray = np.concatenate(results)
    pickle.dump(resultArray, open("result.p", "wb"))
    print("hello")