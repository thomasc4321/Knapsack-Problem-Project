#This code exists to quickly test the algorithms and is not designed for a user or proper maintenance
#Responsibility for timing algorithms could be shifted to this manager script

import random
from datetime import datetime
from bruteforce_ks import b_knapsack_solver
from memoisation_ks import m_knapsack_solver
from tabulation_ks import t_knapsack_solver
from geneticalgorithm_ks import g_knapsack_solver 

def test_algorithm(algorithm):
    start = datetime.now()
    print(algorithm)
    n = 0
    for i in range(1000000):
        n += 1
    end = datetime.now()
    duration = (end - start).total_seconds()
    print(duration)

knapsack_weight = 10
item_amount = 25
item_weights = []
item_values = []
for i in range(item_amount):
    item_values.append(random.randint(1,10))
    item_weights.append(random.randint(1,10))

print(item_values)
print(item_weights)
print()
#print(b_knapsack_solver(item_weights, item_values, knapsack_weight))
test_algorithm(b_knapsack_solver(item_weights, item_values, knapsack_weight))
print()
print(m_knapsack_solver(item_weights, item_values, knapsack_weight))
print()
print(t_knapsack_solver(item_weights, item_values, knapsack_weight))
print()
print(g_knapsack_solver(item_weights, item_values, knapsack_weight, 50, 150, 0.01))
print()
print("####################################################################")
print()