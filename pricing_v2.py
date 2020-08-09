import numpy as np
import math

# parameters
# max look ahead
max_t = 180
# fixed cost per stay
c_x = 150
# variable cost of reservation
c_v = 10
# minium price
min_price = 50
# max_price
max_price = 500
# max length of stay
max_los = 30

time_horizon = list(range(0, max_t))
# possible stays
X = [(t_1, t_2)
     for t_1 in time_horizon for t_2 in time_horizon if t_2 > t_1 and t_2-t_1 <= max_los]


def get_collisions(x, X):
    """takes an individual reservation and the set of reservations
    and returns all resrevations in set that colide with set of reservations
    """
    checkin = x[0]
    checkout = x[1]
    collisions = [(t_1, t_2)
                  for (t_1, t_2) in X if all((t_1 <= checkin, t_2 > checkout))]
    return collisions


def get_cost(x, c_x, c_v):
    """takes reservation, fixed cost, and variable cost (per day)
    and returns nightly cost for res
    """
    los = x[1]-x[0]
    fixed_cost = c_x/los
    total_cost = fixed_cost + c_v
    return total_cost


def get_steepness(los, time_from_now):
    """given los and time from now, it returns the steepness of
    the logistic function for probability given price
    """
    # placeholder
    return 0.04


def get_midpoint(los, time_from_now):
    """given los and time from now, returns the inflection point of logistic
    function for probability given price
    """
    # placeholder
    return 150


def probability_given_price(q, k, m):
    """given a price, and logistic
    function parameters- returns probability of getting booked
    """
    # logistic function
    prob = 1/(1+math.exp(k*(q-m)))
    return prob


def iso_price(x):
    """ get best price for reservation, in isolation
    """
    los = x[1]-x[0]
    time_from_now = x[0]
    # get parameters of logistic function
    # steepness
    k = get_steepness(los, time_from_now)
    # inflection
    m = get_midpoint(los, time_from_now)
    Q = list(range(min_price, max_price))
    iso_price = max([(probability_given_price(q, k, m)*q) for q in Q])
    return iso_price
