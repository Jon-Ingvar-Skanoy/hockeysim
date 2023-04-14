import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange
from scipy.stats import poisson, binom, gamma,betabinom, nbinom
import random
import copy
import tqdm

class Team:
    def __init__(self,name, games_played, goals_for,goals_against,shots_on_goal,shots_against, id):
        self.pi = 0
        self.t = games_played
        self.k = shots_on_goal
        self.binom_a =goals_against
        self.binom_b = shots_against
        self.name = name
        self.poisson_la= (self.t*60)/(self.t*60+1)
        self.points = 0
        self.ma = 0
        self.team3_1 = "a"
        self.team3_2 = "a"
        self.id = id
        self.match_history = []
        
#Antakelse: Det er IKKE høyere sjanse for mål ved "shoutout"
#Antakelse: statistikken vi har inkluderer ikke overtid


def sim_game(team1,team2):
    team1.ma +=1
    team2.ma +=1
    team2.match_history.append(team1.id)
    team1.match_history.append(team2.id)
    shots_team1 = sum(nbinom.rvs(team1.k,(team1.poisson_la),size=60))
    shots_team2 = sum(nbinom.rvs(team2.k,(team2.poisson_la),size=60))
    goals_team1 = betabinom.rvs(shots_team1,team2.binom_a,team2.binom_b)
    goals_team2 = betabinom.rvs(shots_team2,team1.binom_a,team1.binom_b)
    if (goals_team1==goals_team2):
        shots_team1 = sum(nbinom.rvs(team1.k,(team1.poisson_la),size=5))
        shots_team2 = sum(nbinom.rvs(team1.k,(team2.poisson_la),size=5))
        goals_team1 = betabinom.rvs(shots_team1,team2.binom_a,team2.binom_b)
        goals_team2 = betabinom.rvs(shots_team2,team1.binom_a,team1.binom_b)
        if (goals_team1==goals_team2):
            while True:
                goals_team1 = betabinom.rvs(3,team2.binom_a,team2.binom_b)
                goals_team2 = betabinom.rvs(3,team1.binom_a,team1.binom_b)
                if (goals_team1!=goals_team2):
                    break
        if (goals_team1<goals_team2):
            team1.points +=1
            team2.points +=2
            return [1,2]
        if (goals_team1>goals_team2):
            team1.points +=2
            team2.points +=1
            return [2,1]
    if (goals_team1<goals_team2):
        team1.points +=0
        team2.points +=2
        return [0,2]
    if (goals_team1>goals_team2):
        team1.points +=2
        team2.points +=0
        return [2,0]
    
    
def create3matches(division):

    for half in division:
        threematchlist = ["a","a","a"]
        while threematchlist.count("a") != 0:
            threematchlist = []
            for team in half:
                threematchlist.append(team.team3_1)
                threematchlist.append(team.team3_2)        
            tmp1 = ""
            tmp2 = ""
            i=0
            while tmp1 == "" or tmp2 == "":
                if(tmp1==""):
                    if(threematchlist[i] =="a"):
                        tmp1 = i
                elif(tmp2==""):
                    if(threematchlist[i] == "a"):
                        tmp2 = i
                i+=1
            if tmp1%2 == 0:
                tmpvalue1 = int(tmp1/2)
                tmpTeam1 = half[tmpvalue1]
                tmp1secondary = False
            else:
                tmpTeam1 = half[int(round(tmp1/2,0))]
                tmp1secondary = True
            if tmp2%2 == 0:
                tmpTeam2 = half[int(tmp2/2)]
                tmp2secondary = False
            else:
                tmpTeam2 = half[int(round(tmp2/2,0))]
                tmp2secondary = True
            if(tmp1secondary):
                tmpTeam1.team3_2 = tmpTeam2
            else:
                tmpTeam1.team3_1 = tmpTeam2
            if(tmp2secondary):
                tmpTeam2.team3_2 = tmpTeam1
            else:
                tmpTeam2.team3_1 = tmpTeam1

def subdivision_simulation(teams):
    random.shuffle(teams)
    for i in range(0,8):
        if( i != 7):
            sim_game(teams[i],teams[i+1])
            sim_game(teams[i],teams[i+1])
            sim_game(teams[i],teams[i+1])
            for team in teams:
                if (team == teams[i] or team == teams[i+1] or teams[i-1] == team):
                   pass
                   
                else:
                    
                    sim_game(team,teams[i])
                    sim_game(team,teams[i])
               
        else:
            sim_game(teams[i],teams[0])
            sim_game(teams[i],teams[0])
            sim_game(teams[i],teams[0])
            
            for team in teams:
                if (team == teams[i] or team == teams[0] or teams[i-1] == team):
                    pass
                else:
                    
                    sim_game(team,teams[i])
                    sim_game(team,teams[i])
               
    
    
    #for team2 in teams:
    #    tmp = team2.match_history
    #    tmp.sort()
    #    print(len(tmp))
    
def division_simulation(division):
    for team in division[0]:
        for i in range(8):
            sim_game(team, division[1][i])
            sim_game(team, division[1][i])
            sim_game(team, division[1][i])

def interconference_simulation(teams):
    div1 = teams[0]
    div2 = teams[1]
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
    data = pickle.load(open("20-23.p", "rb"))
    names = pickle.load(open("names_20-23.p", "rb"))
    mTeams = []

    aTeams = []
    cTeams = []
    pTeams = []
    eDivision = [mTeams, aTeams]
    wDivision = [cTeams, pTeams]
    teams = [eDivision, wDivision]
    garbagecan = []
    i =0

    #print(len(data))
    #print(len(names))
    for row in data:
        
        tmp = Team(names[i],row[0],row[1],row[2],row[3],row[4], id=i)
        #print(tmp.name)
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
    pickle.dump(teams, open("teams_in_div.p", "wb"))
    return teams
#for division in teams:
#    for alist in division:
#        print(len(alist))
#        for item in alist:
#            print(item.name)
#print("leftovers:")
#for item in garbagecan:
#    print(item.name)


#create3matches(wDivision)
#subdivision_simulation(aTeams)
#subdivision_simulation(mTeams)
#division_simulation(eDivision)

#for team in mTeams:
 #   print(team.team3_1.name)
  #  print(team.team3_2.name)

teams = create_teams()
results = season_simulation_wrapper(teams,1000)
pickle.dump(results, open("result.p", "wb"))
print("hello")