# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 09:56:15 2020

@author: anirudh.madhavan
"""

import simpy
import os
import numpy as np

def warehouse_run(env, order_cutoff, order_target):
    global inventory, balance, num_ordered, total_demand
    inventory = order_target
    balance = 0.00
    num_ordered = 0
    total_demand = 0
    
    while True:
        interarrival = generate_interarrival()
        yield env.timeout(interarrival)
        balance -= inventory*2*interarrival
        demand = generate_demand()
        
        if demand < inventory:
            balance += 100*demand
            inventory -= demand
            print ('{:.2f} sold {}'.format(env.now,demand))
            total_demand +=demand
            #print("Total Demand {}".format(total_demand))
            
        else:
            balance +=100*inventory
            inventory = 0
            print ('{:.2f} Sold out inventory.Out of stock {} inventory'.format(env.now,inventory))
        if inventory < order_cutoff and num_ordered == 0:
            env.process(handle_order(env, order_target))

def handle_order(env, order_target):
    global inventory, balance, num_ordered
    
    
    num_ordered = order_target - inventory
    print ('{:.2f} placed order {}'.format(env.now,num_ordered))
    balance = 50*num_ordered
    yield env.timeout(2.0) # wait for 2 days 
    inventory += num_ordered
    num_ordered = 0
    print ('{:.2f} received order {} in inventory'.format(env.now,inventory))
            
              
def generate_interarrival():
    return np.random.exponential(1./5) ## This is to take care of customers coming in everyday. ##

def generate_demand():
    return np.random.randint(1,5) ## to satisfy uniform demand

obs_time = []
inventory_level = []

def observe(env):
    global invetory
    while True:
        obs_time.append(env.now)
        inventory_level.append(inventory)
        yield env.timeout(0.1)

np.random.seed(0)

env = simpy.Environment()
env.process(warehouse_run(env, 20, 50))
env.process(observe(env))

env.run(until = 5.0)

import matplotlib.pyplot as plt

plt.figure()
plt.step(obs_time, inventory_level, where="post")
plt.xlabel("simulation days")
plt.ylabel("INV Level")
