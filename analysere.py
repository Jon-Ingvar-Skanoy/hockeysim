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
data = pickle.load(open("result.p", "rb"))
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

fig = px.histogram(winnernames,histnorm='probability')

fig.show()      