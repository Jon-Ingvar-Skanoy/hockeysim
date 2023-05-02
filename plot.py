import pickle

from scipy.stats import gamma,betabinom, nbinom, beta
import plotly.express as px
import plotly.io as io
import numpy as np
io.renderers.default = "browser"

class Team:     #definiasjon av team classen se sim.py for mer info
    def __init__(self,name, games_played, goals_for,goals_against,shots_on_goal,shots_against, id):
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



plot = 4      # instilling for hvilke plot som skal plottes, 0 = alle, 1 = postiroir sansynlighetsfordeling i poisson prosses, 2 = prediktiv sansynlighetsfordeling i poisson prosses,  3 = postiroir sansynlighetsfordeling i Berunulli prosses, 4 = prediktiv sansynlighetsfordeling i Berunulli prosses

target_teams = [mulige_lag[0],'Arizona Coyotes',"Chicago Blackhawks",'Vegas Golden Knights']        # liste med navn på hvilke lag som skal plottes, ved tom liste plottes alle lag, anbefales sterk å begrense hvilke lag. mulige lag er hjelpevariabel for å velge lag.

xp= np.arange(0,90,1)

        
for Conference in data:
    for Division in Conference:
            for team in Division: # hvor å kjøre gjennom alle lagene
                
                if(plot ==1 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):

                        xp= np.arange(0,80,1)
                        posterior_distrubution = gamma.pdf(xp,team.k/(team.t), loc = 0,scale=1)
                        fig = px.line(y=posterior_distrubution*80/len(posterior_distrubution), x=xp,title=team.name)
                        print(sum(posterior_distrubution*80/len(posterior_distrubution)))
 
                        #Beregner 90% intervallestimat
                        lower_bound = gamma.ppf(0.05,team.k/(team.t), scale=1)
                        upper_bound = gamma.ppf(0.95,team.k/(team.t), scale=1)
                        middle_bound = gamma.ppf(0.5,team.k/(team.t), scale=1)
                        ninety_percent_interval = upper_bound-lower_bound

                        #Markerer graf med intervallestimat, og skalerer grafen så den ikke ser helt uleselig ut når den genereres
                        fig.add_vline(lower_bound, line_color="maroon")
                        fig.add_vline(upper_bound, line_color="maroon")
                        fig.add_vline(middle_bound, line_color="maroon",annotation_text=('Forventet verdi:%.2f'%middle_bound ))
                        fig.update_xaxes(range=[lower_bound-ninety_percent_interval, upper_bound+ninety_percent_interval])
                        fig.show()

                        
                if(plot ==3 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):
                        xp= np.arange(0,1,0.00002)

                        posterior_distrubution = beta.pdf(xp,team.binom_a,team.binom_b, loc=0, scale=1)
                        fig = px.line(y=posterior_distrubution/(len(posterior_distrubution)), x=xp,title=team.name)
                        print(sum(posterior_distrubution/(len(posterior_distrubution))))

                        #Beregner 90% intervallestimat
                        lower_bound = beta.ppf(0.05,team.binom_a,team.binom_b, loc=0, scale=1)
                        upper_bound = beta.ppf(0.95,team.binom_a,team.binom_b, loc=0, scale=1)
                        middle_bound = beta.ppf(0.5,team.binom_a,team.binom_b, loc=0, scale=1)
                        ninety_percent_interval = upper_bound-lower_bound

                        #Markerer graf med intervallestimat, og skalerer grafen så den ikke ser helt uleselig ut når den genereres
                        fig.add_vline(lower_bound, line_color="maroon")
                        fig.add_vline(upper_bound, line_color="maroon")
                        fig.add_vline(middle_bound, line_color="maroon",annotation_text=('Forventet verdi:%.3f'%middle_bound ))
                        fig.update_xaxes(range=[lower_bound-ninety_percent_interval, upper_bound+ninety_percent_interval])
                        fig.update_yaxes(range=[0,max(posterior_distrubution/len(posterior_distrubution))*1.1])
                        fig.show()

                if(plot ==2 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):
                        xp= np.arange(5,60,1)

                        predictive_distrubution = nbinom.pmf(xp,team.k,(team.t/(team.t+1)), loc = 0)
                        fig = px.line(y=predictive_distrubution, x=xp,title=team.name)
                        print(sum(predictive_distrubution))
 
                        #Beregner 90% intervallestimat
                        lower_bound = nbinom.ppf(0.05,team.k,(team.t/(team.t+1)))
                        upper_bound = nbinom.ppf(0.95,team.k,(team.t/(team.t+1)))
                        middle_bound = nbinom.ppf(0.5,team.k,(team.t/(team.t+1)))
                        ninety_percent_interval = upper_bound-lower_bound

                        #Markerer graf med intervallestimat, og skalerer grafen så den ikke ser helt uleselig ut når den genereres
                        fig.add_vline(lower_bound, line_color="maroon")
                        fig.add_vline(upper_bound, line_color="maroon")
                        fig.add_vline(middle_bound, line_color="maroon",annotation_text=('Forventet verdi:%.0f'%middle_bound ))
                        fig.update_xaxes(range=[lower_bound-ninety_percent_interval, upper_bound+ninety_percent_interval])
                        fig.update_yaxes(range=[0,max(predictive_distrubution/len(predictive_distrubution))*1.1])
                        fig.show()

                     
                
                if(plot ==4 or plot == 0):
                    if(team.name in target_teams or len(target_teams)==0):
                            xp = np.arange(40,150,1)
                            predictive_distrubution = betabinom.pmf(xp,1000,team.binom_a,team.binom_b, loc=0)
                            fig = px.line(y=predictive_distrubution, x=xp/1000,title=team.name)
                            print(sum(predictive_distrubution))

                            #Beregner 90% intervallestimat
                            lower_bound = betabinom.ppf(0.05,1000,team.binom_a,team.binom_b, loc=0)/1000
                            upper_bound = betabinom.ppf(0.95,1000,team.binom_a,team.binom_b, loc=0)/1000
                            middle_bound = betabinom.ppf(0.5,1000,team.binom_a,team.binom_b, loc=0)/1000
                            ninety_percent_interval = upper_bound-lower_bound

                            #Markerer graf med intervallestimat, og skalerer grafen så den ikke ser helt uleselig ut når den genereres
                            fig.add_vline(lower_bound, line_color="maroon")
                            fig.add_vline(upper_bound, line_color="maroon")
                            fig.add_vline(middle_bound, line_color="maroon",annotation_text=('Forventet verdi:%.4f'%middle_bound ))
                            fig.update_xaxes(range=[lower_bound-ninety_percent_interval, upper_bound+ninety_percent_interval])
                            fig.update_yaxes(range=[0,max(predictive_distrubution/len(predictive_distrubution))*1.1])
                            fig.show()
                       
                

                
                

                







    