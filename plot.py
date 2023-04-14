import pickle
from numba import jit, prange
from scipy.stats import poisson, binom, gamma,betabinom, nbinom
import random
import copy
import tqdm
import plotly.express as px
import plotly.io as io
class Team:
    def __init__(self,name, games_played, goals_for,goals_against,shots_on_goal,shots_against, id):
        self.pi = 0
        self.t = games_played
        self.k = shots_on_goal
        self.binom_a =goals_for
        self.binom_b = shots_on_goal
        self.name = name
        self.poisson_la= (self.t*60)/(self.t*60+1)
        self.points = 0
        self.ma = 0
        self.team3_1 = "a"
        self.team3_2 = "a"
        self.id = id
        self.match_history = []


data = pickle.load(open("teams_in_div.p", "rb"))
size1 = 10000

for Conference in data:
    for Division in Conference:
            for team in Division:
                #df = poisson.rvs(mu =(team.k/team.t),size=size1)
                #fig = px.histogram(df,histnorm='probability',title=team.name)
                #fig.show()
                #df = binom.rvs(1000, p = (team.binom_a/team.binom_b), size = size1)/1000
                #fig = px.histogram(df,histnorm='probability',title=team.name)
                #fig.show()
                df = []
                for i in range(10000):
                    df.append(sum(nbinom.rvs(team.k,(team.poisson_la),size=60)))
                fig = px.histogram(df,histnorm='probability',title=team.name)
                fig.show()
                
                #df = betabinom.rvs(1000,team.binom_a,team.binom_b, size = 10000)/1000
                #fig = px.histogram(df,histnorm='probability',title=team.name)
                #fig.show()

                




#for i in range(46):
   # df = poisson.rvs(mu =(data[i,3]/data[i,0]),size=size1)
    #fig = px.histogram(df,histnorm='probability',title=names[i])
    #fig.show()
    #df = binom.rvs(1000, p = ( data[i,2]/data[i,4]), size = size1)/1000
    #fig = px.histogram(df,histnorm='probability',title=names[i])
    #fig.show()


    