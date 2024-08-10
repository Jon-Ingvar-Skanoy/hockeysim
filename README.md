# Simulating NHL Seasons Using Statistical Methods

## Project Overview

This project focuses on simulating NHL (National Hockey League) seasons using advanced statistical methods, including Poisson and Bernoulli processes. The simulation leverages historical data from the NHL and attempts to predict outcomes for the 2023-2024 season based on these statistical models.

## Authors

- **Jon Ingvar Skånøy**
- **Isak Killingrød**

This project was completed as part of the MA-223-G course in the Spring of 2023.

## Introduction

The project aims to simulate hockey games and entire seasons using statistical methods. Given the availability of detailed data, hockey presents an interesting challenge due to the sport's complexity and the multiple possible outcomes of each game.

### Simulation Method

Two statistical processes were employed:
1. **Poisson Process**: To simulate the number of shots on goal during a game.
2. **Bernoulli Process**: To determine the probability of each shot resulting in a goal, based on the opposing team's defensive performance.

### Data Source

Historical data from the NHL seasons between 2010-2023 was obtained from [Hockey Reference](https://www.hockey-reference.com/leagues/NHL_2023.html). This data provided the basis for the simulation, allowing for an informed prediction of game outcomes.

## Data Collection

The data collected for each team included:
- **Games Played**: Number of games played by the team, used in the Poisson process.
- **Goals Against**: Number of goals scored against the team, used in the Bernoulli process.
- **Shots on Goal**: Number of shots taken by the team.
- **Shots Against**: Number of shots faced by the team.

The data was cleaned and imported using Python scripts, with older seasons weighted less heavily than more recent ones.

## Statistical Methods

### Posterior Probability Distributions

The project focused on two key distributions:
1. **Poisson Distribution**: Used to predict the number of shots a team will take in a game.
2. **Bernoulli Distribution**: Used to predict the likelihood of those shots resulting in goals.

### Predictive Probability Distributions

For the 2023-2024 season simulation, the following distributions were utilized:
- **Beta-Binomial Distribution**: To predict the number of goals conceded by a team.
- **Negative Binomial Distribution**: To predict the number of shots on goal a team will take.

## Code Description

The project is implemented in Python, with several key scripts:
- **input.py**: Imports and cleans the raw data from CSV files.
- **combine.py**: Combines multiple seasons' data into a single dataset with appropriate weighting.
- **sim.py**: Runs the simulation of games and entire seasons.
- **plot.py**: Generates plots of the statistical distributions and simulation results.
- **analysere.py**: Analyzes the simulation results, including team rankings and season outcomes.

### Key Functions

- **sim_game()**: Simulates an individual hockey game.
- **season_simulation()**: Simulates an entire NHL season.
- **get_winners()**: Determines the season's winners based on simulation results.

## Results

The simulation produced realistic results, with teams like the Boston Bruins and Vegas Golden Knights consistently performing well, while teams like Seattle Kraken and Arizona Coyotes underperformed.

### Conclusion

The project demonstrates how statistical models can effectively simulate sports seasons, providing insights into team performance and potential outcomes. While the simulation is robust, there are areas for improvement, such as incorporating more granular data or refining the models used.

### Potential Improvements

Future work could involve:
- Simulating at the player level to increase accuracy.
- Incorporating specific team matchups rather than treating all games as independent events.

## How to Run the Project

1. Clone this repository.
2. Install the necessary Python libraries using `pip`.
3. Run `input.py` to load and preprocess the data.
4. Use `sim.py` to run the simulations.
5. Analyze results using `analysere.py`.

## Bibliography

- Nyberg, S. O. (2019). *The Bayesian Way* (1st ed.). John Wiley Sons, Inc.
- Hockey Reference (2023). [NHL Historical Data](https://www.hockey-reference.com/leagues/NHL_2023.html).

