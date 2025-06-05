from datetime import datetime

def t_knapsack_solver(item_weights, item_values, knapsack_weight):
    """Solves a knapsack problem using tabulation, returns answer and runtime

    Items are represented through two lists: the weights and values.
    """
    start = datetime.now()

    item_amount = len(item_weights)

    #table iteratively filled to reach optimal solution at position [-1][-1]
    stored_values = [[0 for i in range(knapsack_weight+1)] for j in range(item_amount+1)]

    #iterates through each element in the list
    for item in range(0, item_amount+1):
        for weight in range(0, knapsack_weight+1):
            #sets the first row and column to 0, so following entries can build off of them
            if item == 0 or weight == 0:
                stored_values[item][weight] = 0
            #if the current item can fit into the knapsack
            elif item_weights[item-1] <= weight:
                #the value of the item + best previous value with corresponding weight capacity
                value_if_item_added = item_values[item-1] + stored_values[item-1][weight - item_weights[item-1]]
                stored_values[item][weight] = max(value_if_item_added, stored_values[item-1][weight])
            else:
                #if a new item cannot be added, value is same as before
                stored_values[item][weight] = stored_values[item-1][weight]
            
    max_value = stored_values[-1][-1]

    end = datetime.now()
    time_difference = (end - start).total_seconds()
    return max_value, time_difference