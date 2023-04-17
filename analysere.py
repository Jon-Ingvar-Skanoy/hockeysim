import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange
from scipy.stats import poisson, binom, gamma,betabinom
import random
import copy
import tqdm
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
data = pickle.load(open("result.p", "rb"))

def get_winners(data):
    # function that find the winner of every season and putt the winner names in a list
    winnernames = []
    for season in data:
        max = tmp = Team(0,0,0,0,0,0,0)
        for Conference in season:
            for Division in Conference:
                for team in Division:
                    
                    #print(team.points, team.name)
                    if(team.points > max.points):
                        max = team
        print(max.name,max.points)
        winnernames.append(max.name)
    return winnernames

def get_total_points(data):
    # function that sums upp the points each team gets ill ass simulated seasons
    total_points = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for season in data:
        for conference in season:
            for division in conference:
                for team in division:
                    total_points[team.id] += team.points
    return total_points

def get_avg_ranking(data):
    # function that gets the avrange rating for each team in all ratings and also return a list with all the rancking of every team
    standings_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    avg_standings_list = []
    for season in data:
        new_conferences = []
        for conference in season:
            new_conference = np.concatenate(conference)
            new_conferences.append(new_conference)
        new_season = np.concatenate(new_conferences)

        standings = sorted(new_season,key=lambda x: x.points, reverse=True)
        for i in range(32):
            team = standings[i]
            standings_list[team.id].append(int(i+1))
    for i in range(32):
        #print(standings_list[i])
        #print(len(standings_list[i]))
        average = np.mean(standings_list[i])
        avg_standings_list.append(average)
    return avg_standings_list, standings_list



# print information about the points
points = get_total_points(data)
print(points)
mean = sum(points)/32
print("mean:", mean)

standard_deviation = 0
for x in points:
    standard_deviation += (x-mean)**2
standard_deviation = standard_deviation/32
standard_deviation = standard_deviation**0.5
print("sd:", standard_deviation)
print("worst:", min(points),points.index(min(points)))
print("best:", max(points))
names = ["Boston Bruins", "Carolina Hurricanes","New Jersey Devils","Vegas Golden Knights","Toronto Maple Leafs","New York Rangers","Edmonton Oilers","Colorado Avalanche",
         "Dallas Stars","Los Angeles Kings","Minnesota Wild","Seattle Kraken","Tampa Bay Lightning", "Winnipeg Jets", "Florida Panthers","New York Islanders",
         "Calgary Flames","Nashville Predators", "Pittsburgh Penguins", "Buffalo Sabres","Ottawa Senators","Vancouver Canucks","St. Louis Blues","Detroit Red Wings",
         "Washington Capitals","Philadelphia Flyers","Arizona Coyotes","Montreal Canadiens","San Jose Sharks","Chicago Blackhawks", "Anaheim Ducks","Columbus Blue Jackets"]

#plot pie chart of point distrobution

point_fig = px.pie(values = points,title = "Total points per team", names = names)
point_fig.show()

avg_ranks, all_ranks = get_avg_ranking(data)
print(avg_ranks)
# plot avrange ranging
avg_fig = px.bar(x=names, y=avg_ranks, title="Average ranking")
avg_fig.show()
# plots all ranking distrobution plots
for i in range(32):
    team_hist_fig = px.histogram(all_ranks[i],histnorm="probability",  title=names[i])
    team_hist_fig.show()
#plot wich teams won most seasons
winnernames = get_winners(data)
fig = px.histogram(winnernames,histnorm='probability')
fig.show()      