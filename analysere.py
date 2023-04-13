import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange
from scipy.stats import poisson, binom, gamma,betabinom
import random
import copy
import tqdm

s1 = pickle.load(open("result.p", "rb"))