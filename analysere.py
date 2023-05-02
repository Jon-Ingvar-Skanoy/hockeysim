import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from scipy.stats import poisson, binom, gamma,betabinom, beta
import random
import copy

#Liste der navn har lik indeks som lag-ID brukt i programmet
names = ["Boston Bruins", "Carolina Hurricanes","New Jersey Devils","Vegas Golden Knights","Toronto Maple Leafs","New York Rangers","Edmonton Oilers","Colorado Avalanche",
         "Dallas Stars","Los Angeles Kings","Minnesota Wild","Seattle Kraken","Tampa Bay Lightning", "Winnipeg Jets", "Florida Panthers","New York Islanders",
         "Calgary Flames","Nashville Predators", "Pittsburgh Penguins", "Buffalo Sabres","Ottawa Senators","Vancouver Canucks","St. Louis Blues","Detroit Red Wings",
         "Washington Capitals","Philadelphia Flyers","Arizona Coyotes","Montreal Canadiens","San Jose Sharks","Chicago Blackhawks", "Anaheim Ducks","Columbus Blue Jackets"]
def print_names_and_indexes(names):
    for i in range(32):
        print("Team name: ", names[i], "ID/Index: ", i)

#Gjenbrukt klasse fra sim.py. Formaten datafilen vår er lagret i.
class Team:
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
data = pickle.load(open("result.p", "rb"))


#I tilfelle to lag har nøyaktig samme poengsum på slutten av en sesong er det et par tiebreaks som brukes
#Vi bruker omtrent samme regler som NHL, med noen "abstraksjoner" gjort pga manglende data for et par punkter
#Hvis to lag har like mange poeng, så sjekker vi først om et lag har vunnet flere kamper enn det andre.
#Om det er likt, så sjekker vi hvilket lag som slo det andre flest ganger
#Om det er likt, så tar vi et myntkast. Hvis man fjerner # fra linje 55 og bytter det om til if get_match_history(data,team1.id,team2.id, False):
#så vil det gjøres tilfeldig uttrekk fra en prediktiv fordeling i stedet, som gir oss et potensielt resultat på en kamp mellom lagene. Nedsiden med denne metoden er at
#man må være beredt på at å kjøre programmet i svært lang tid for å få noen resultater med den metoden slik vi har kodet den 
def tiebreak(team1, team2):
    winner = 0
    if len(team1.beaten) > len(team2.beaten):
        winner = team1
    elif len(team1.beaten) < len(team2.beaten):
        winner = team2
    elif len(team1.beaten) == len(team2.beaten):
        if team1.beaten.count(team2.id) > team2.beaten.count(team1.id):
            winner = team1
        elif team1.beaten.count(team2.id) < team2.beaten.count(team1.id):
            winner = team2
        elif team1.beaten.count(team2.id) == team2.beaten.count(team1.id):
            #Totalt antall myntkast gjort for å avgjøre alle plasseringene for alle sesongene er 88844, som er 2.3% av alle plasseringene.
            #For førsteplass spesifikkt er 941 førsteplasser avgjort av myntkast, ut av 120,000, som er 0.78%.

            coinflip = random.randint(0,1)
            if coinflip == 0:#(get_match_history(data, team1.id, team2.id, False)):
                winner = team1
            else:
                winner = team2
    return winner
            

def get_winners(data):
    #Liste for navnet til vinnerlaget i hver sesong
    winnernames = []
    for season in data:
        max = Team(0,0,0,0,0,0,0)
        for Conference in season:
            for Division in Conference:
                for team in Division:
                    
                    #Oppdaterer en tmp-verdi for å bli lik det beste laget så langt
                    if(team.points > max.points):
                        max = team
                    #I tilfelle at to lag har like mange poeng, og har førsteplass (10% av simulerte sesonger, sånn circa), så følger vi litt 
                    #abstraherte tiebreak-regler fra NHL:
                    #Gitt at det er like mange poeng etter like mange kamper, så vinner laget som har vunnet flest kamper, så vi ser
                    #på lengden av lista med lag som har blitt slått
                    #Om det er likt, så går det til laget som har vunnet flest kamper mot det andre laget (untatt kamper i overtid, som vi ikke kan se forskjell på)
                    elif(team.points == max.points):
                        max = tiebreak(max,team)
                        
        winnernames.append(max.name)
    print(winnernames.count("Tie"))
    #Histogram som viser fordelingen av førsteplasser
    fig = px.histogram(winnernames,histnorm='probability', title= "Percentage of seasons won by each team")
    fig.show()      

def get_total_points(data):
    total_points = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #Les inn poengene fra hvert lagobjekt i hver sesong
    for season in data:
        for conference in season:
            for division in conference:
                for team in division:
                    total_points[team.id] += team.points
    
    #Beregner standardavviket på poeng
    standard_deviation_of_points = np.std(total_points)
    print("sd, total points:", standard_deviation_of_points)

    #Printer ut beste og verste lag, poengmessig
    print("Lowest total of points:", min(total_points),"ID/index: ", total_points.index(min(total_points)))
    print("Highest total of points:", max(total_points),"ID/index: ", total_points.index(max(total_points)))


    #Plotter kakediagram og stolpediagram av poengfordeling
    point_fig = px.pie(values = total_points,title = "Total points per team", names = names)
    point_fig.show()
    point_fig_pole = px.bar(y=total_points, title = "Total points per team",x=names)
    point_fig_pole.show()

def get_avg_ranking(data):
    #Genererer 32 lister, en for plasseringene til hvert lag
    standings_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    avg_standings_list = []
    for season in data:
        new_conferences = []
        #Slår sammen alle 32 lagene i en sesong til en liste
        for conference in season:
            new_conference = np.concatenate(conference)
            new_conferences.append(new_conference)
        new_season = np.concatenate(new_conferences)

        #Sorterer listen for å finne laget med flest poeng
        standings = sorted(new_season,key=lambda x: x.points, reverse=True)


        #Avgjør rangeringer for lag med like mange poeng, ved å loope gjennom og sjekke to av gangen. 
        #Om de har samme poengsum og laget med høyere indeks vinner tiebreak, bytt lagene.
        for i in range(31):
            if standings[i].points == standings[i+1].points:
                if standings[i].id != tiebreak(standings[i],standings[i+1]).id:
                    standings[i], standings[i+1] = standings[i+1], standings[i]
        for i in range(32):
            team = standings[i]
            #Listeindeks går fra 0-31, og plassering går fra 1-32, så plassering er lik indeks+1
            standings_list[team.id].append(int(i+1))
    
    #Finner gjennomsnittsrangeringen til lagene
    for i in range(32):
        average = np.mean(standings_list[i])
        avg_standings_list.append(average)
    print("Average ranks per team", avg_standings_list)
    avg_fig = px.bar(x=names, y=avg_standings_list, title="Average ranking")
    avg_fig.show()

    #Finner standardavviket mellom gjennomsnittsrangeringene til alle lagene
    standard_deviation_of_ranks = np.std(avg_standings_list)
    print("Standard deviation of average rank:",standard_deviation_of_ranks)

    #Finner standardavviket på plasseringer til individuelle lag
    sdlist = []
    for i in range(32):
        print("Standard deviation in ranks for", names[i], ":", np.std(standings_list[i]))
        sdlist.append(np.std(standings_list[i]))
    for i in range(32):
        team_hist_fig = px.histogram(standings_list[i],histnorm="probability",  title="Ranking histogram for "+names[i])
        team_hist_fig.show()
    sd_rankings_fig = px.bar(y=sdlist, x=names, title="Standard deviation of ranks per team")
    sd_rankings_fig.show()

    #Sorterer lagene etter poeng ved å sammenlikne indeks av gjennomsnittsrank mellom liste sortert etter beste gjennomsnittsrank og liste sortert etter lag-ID
    #Viser samme informasjon som grafen over, men er penere for rapporten
    sorted_rankings = sorted(copy.deepcopy(avg_standings_list))
    sorted_std = []
    sorted_names = []
    for i in range(32):
        sorted_std.append(sdlist[avg_standings_list.index(sorted_rankings[i])])
        sorted_names.append(names[avg_standings_list.index(sorted_rankings[i])])
    sorted_sd_rankings_fig = px.bar(y=sorted_std, x=sorted_names, title="Standard deviation of ranks per team, sorted by average team ranking")
    sorted_sd_rankings_fig.show()    

def get_match_history(data, team1_id, team2_id, graph):
    #Funksjon for å hente ut antallet ganger lag 1 har slått lag 2 og omvendt
    team1_win_counter = 0
    team2_win_counter = 0

    for simulated_season in data:
        #Leter ut hvert objekt som representerer lag 1 og lag 2 i hver sesong, og legger til seierene hvert lag har mot hverandre
        for division in simulated_season:
            for subdivision in division:
                for team in subdivision:
                    #Hvert lag har en ID, og en liste med IDer. Når et lag slår et annet i simuleringen,
                    #blir IDen til laget som tapte lagt til i listen til vinnerlaget.
                    #Denne loopen henter ut antallet ganger det ene laget har IDen til det andre laget i listen sin
                    if team.id == team1_id:
                        team1_win_counter += team.beaten.count(team2_id)
                    elif team.id == team2_id:
                        team2_win_counter += team.beaten.count(team1_id)

    #graph = True om vi skal generere grafer, og er false om vi kun skal ha litt informasjon
    if graph:       
        print("Amount of times %s beat %s: "%(names[team1_id], names[team2_id]), team1_win_counter)
        print("Amount of times %s beat %s: "%(names[team2_id], names[team1_id]), team2_win_counter)

        #Plotter posterior pdf som viser verdiene pi kan realistisk ha
        xp= np.arange(0,1,0.00002)

        posterior_distrubution_of_pi = beta.pdf(xp,team1_win_counter,team2_win_counter)
        pi_distribution_fig = px.line(y=posterior_distrubution_of_pi/len(posterior_distrubution_of_pi), x=xp, title= "Posterior distribution for pi, where pi represents the chances of %s beating %s"%(names[team1_id], names[team2_id]))
        print(sum(posterior_distrubution_of_pi/len(posterior_distrubution_of_pi)))

        #Beregner 90% intervallestimat
        lower_bound = beta.ppf(0.05,team1_win_counter,team2_win_counter)
        upper_bound = beta.ppf(0.95,team1_win_counter,team2_win_counter)
        ninety_percent_interval = upper_bound-lower_bound

        #Markerer graf med intervallestimat, og skalerer grafen så den ikke ser helt uleselig ut når den genereres
        pi_distribution_fig.add_vline(lower_bound, line_color="maroon")
        pi_distribution_fig.add_vline(upper_bound, line_color="maroon")
        pi_distribution_fig.update_xaxes(range=[lower_bound-ninety_percent_interval, upper_bound+ninety_percent_interval])
        pi_distribution_fig.show()
    else:
        #Denne delen var skrevet for at get_match_history kan kalles i tiebreak-funksjonen. Om man erstatter myntkastet med funksjonskallet for denne funksjonen,
        #så vil det gjøre tilfeldig uttak fra prediktiv fordeling basert på hvordan det har gått mellom lagene i alle simuleringene.
        #Funksjonen ble ikke brukt i det endelige programmet, fordi den legger til mange minutter på kjøretiden til programmet
        tmp = betabinom.rvs(1,team1_win_counter,team2_win_counter)
        return tmp 

    
    

#Main-delen av programmet. Kan kommentere ut funksjonskall om man bare er interessert i et resultat, slik at man 
#slipper unna å grave gjennom 35 urelaterte grafer etter det man vil ha

#get_total_points(data)
get_match_history(data, 24, 5, True)
#get_winners(data)
#get_avg_ranking(data)
