import pickle
from numba import prange
from scipy.stats import gamma,betabinom, nbinom, beta
import plotly.express as px
import plotly.io as io
import numpy as np
io.renderers.default = "browser"

class Team:     #definiasjon av team classen se sim.py for mer info
    def __init__(self,name, games_played, goals_for,goals_against,shots_on_goal,shots_against, id):
        self.pi = 0
        self.t = games_played
        self.k = shots_on_goal
        self.binom_a =goals_against
        self.binom_b = shots_against- self.binom_a
        self.name = name
        self.poisson_la= (self.t*60)/(self.t*60+1)
        self.points = 0
        self.ma = 0
        self.team3_1 = "a"
        self.team3_2 = "a"
        self.id = id
        self.match_history = []
        self.beaten = []

data = pickle.load(open("teams_in_div.p", "rb")) # henter data fra sim.py
mulige_lag = ['Boston Bruins', 'Carolina Hurricanes', 'New Jersey Devils', 'Vegas Golden Knights', 'Toronto Maple Leafs', 'New York Rangers', 'Edmonton Oilers', 'Colorado Avalanche', 'Dallas Stars', 'Los Angeles Kings', 'Minnesota Wild', 'Seattle Kraken', 'Tampa Bay Lightning', 'Winnipeg Jets', 'Florida Panthers', 'New York Islanders', 'Calgary Flames', 'Nashville Predators', 'Pittsburgh Penguins', 'Buffalo Sabres', 'Ottawa Senators', 'Vancouver Canucks', 'St. Louis Blues', 'Detroit Red Wings', 'Washington Capitals', 'Philadelphia Flyers', 'Arizona Coyotes', 'Montreal Canadiens', 'San Jose Sharks', 'Chicago Blackhawks', 'Anaheim Ducks', 'Columbus Blue Jackets', 'Phoenix Coyotes', 'Atlanta Thrashers']


size1 = 100000           # datapunkt for hvor mye data vi pruker i plottene
plot = 1                 # instilling for hvilke plot som skal plottes, 0 = alle, 1 = postiroir sansynlighetsfordeling i poisson prosses, 2 = prediktiv sansynlighetsfordeling i poisson prosses,  3 = postiroir sansynlighetsfordeling i Berunulli prosses, 4 = prediktiv sansynlighetsfordeling i Berunulli prosses
target_teams = [mulige_lag[0],'Carolina Hurricanes']        # liste med navn på hvilke lag som skal plottes, ved tom liste plottes alle lag, anbefales sterk å begrense hvilke lag. mulige lag er hjelpevariabel for å velge lag.


for Conference in data:
    for Division in Conference:
            for team in Division: # hvor å kjøre gjennom alle lagene
                
                if(plot ==1 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):
                        df = []
                        for i in prange(size1): # for å lage liste med mange datapunkter med 60 opservasjoner. 
                            df.append(sum(gamma.rvs(team.k/(team.t*60),size=60)))
                        fig = px.histogram(df,histnorm='probability',title=team.name) # plotting av datapunktene med mean og  mean+- standard deviation

                        fig.add_vline(np.mean(df), name="mean",line_color="maroon",annotation_text="mean =" + str(np.mean(df).round(1)))
                        fig.add_vline(np.mean(df)+np.std(df), line_color='maroon',annotation_text="std")
                        fig.add_vline(np.mean(df)-+np.std(df), line_color='maroon',annotation_text="std")
                    
                        fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))
                        fig.show()
                
                if(plot ==3 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):
                        df = beta.rvs(team.binom_a,team.binom_b, size = size1)# for å lage liste med datapunkter med 1 observasjon 
                        fig = px.histogram(df,histnorm='probability',title=team.name) # plotting av datapunktene med mean og  mean+- standard deviation

                        fig.add_vline(np.mean(df), name="mean",line_color="maroon",annotation_text="mean =" + str(np.mean(df).round(1)))
                        fig.add_vline(np.mean(df)+np.std(df), line_color='maroon',annotation_text="std")
                        fig.add_vline(np.mean(df)-+np.std(df), line_color='maroon',annotation_text="std")
                        fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))
                        fig.show()
                if(plot ==2 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):
                        df = []
                        for i in prange(size1):  # for å lage liste med mange datapunkter med 60 opservasjoner. 
                            df.append(sum(nbinom.rvs(team.k,(team.poisson_la),size=60)))
                        fig = px.histogram(df,histnorm='probability',title=team.name) # plotting av datapunktene med mean og  mean+- standard deviation
                        fig.add_vline(np.mean(df), name="mean",line_color="maroon",annotation_text="mean =" + str(np.mean(df).round(1)))
                        fig.add_vline(np.mean(df)+np.std(df), line_color='maroon',annotation_text="std")
                        fig.add_vline(np.mean(df)-+np.std(df), line_color='maroon',annotation_text="std")
                        fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))
                        fig.show()
                
                if(plot ==4 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):
                        df = betabinom.rvs(10000,team.binom_a,team.binom_b, size = 100000)/10000 # for å lage liste med datapunkter med 1 observasjon 
                        fig = px.histogram(df,histnorm='probability',title=team.name)# plotting av datapunktene med mean og  mean+- standard deviation
                        fig.show()
                        fig.add_vline(np.mean(df), name="mean",line_color="maroon",annotation_text="mean =" + str(np.mean(df).round(1)))
                        fig.add_vline(np.mean(df)+np.std(df), line_color='maroon',annotation_text="std")
                        fig.add_vline(np.mean(df)-+np.std(df), line_color='maroon',annotation_text="std")
                        fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))
                        fig.show()
                

                
                

                







    