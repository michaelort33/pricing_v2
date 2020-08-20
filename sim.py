# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 19:45:08 2020

@author: Teddy
"""
import numpy as np
from itertools import permutations
import networkx as nx
from scipy.special import lambertw

#%% Setup functions
def collides(x1,x2):
    return x1[0] < x2[1] and x1[1] > x2[0] and x1 != x2

def res_len(x):
    """ The length of a single reservation or array of reservations """
    return x[1]-x[0] if isinstance(x, tuple) else np.sum(np.asarray(x)*[-1,1],1)
    
#%% Define the problem
t = 30   # Number of days

def p(q, x):
    """ Specify the isolated probability as a function of daily price and reservation """
    return 1 /(1 + np.exp((q-100)/10))

def q(x):
    """ Specify the daily price for each reservation """
    return 100
    # return np.real(10*lambertw(np.exp(100/10-1))+10) # Optimal isolated price from logistic function

#%% Calculate reservation space and collision matrix
X = [(a,b) for a,b in permutations(range(t), 2) if a<b]
A = np.apply_along_axis(lambda x: collides(X[x[0]],X[x[1]]), 0, np.meshgrid(range(len(X)),range(len(X))))

#%% Simulate
n = 1000  # Number of times to simulate

Q = [q(x) for x in X] # evaluate nightly prices
P = [p(q,x) for q,x in zip(Q,X)] # Use prices to find isolated probabilities
req = np.random.rand(n, len(X)) < P # n trials of reservation requests
order = np.stack([np.random.permutation(len(X)) for i in range(n)]) # n trials of precedence

for i in order.T:
    r = req[range(n),i]
    req[r] &= ~A[:,i].T[r]
        
Ev = np.sum(req.mean(0) * Q * res_len(X)) # prob * nightly price * len_of_stay
Eocc = np.mean([np.sum(res_len(np.array(X)[x])) for x in req])/t
Elos = np.mean([np.mean(res_len(np.array(X)[x])) if np.any(x) else 0 for x in req])

#%% Display as a graph
# G = nx.Graph(A)
# nx.draw(G, pos=list(zip(np.array(X).mean(1), np.sum(np.array(X)*[-1,1], 1)**2)))