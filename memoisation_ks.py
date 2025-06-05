from datetime import datetime

def m_knapsack_solver(item_weights, item_values, knapsack_weight):
    """Solves a knapsack problem using memoisation, returns answer and runtime

    Items are represented through two lists: the weights and values.
    """
    start = datetime.now()

    knapsack_value = 0
    item_amount = len(item_weights)

    #holds previously reached solutions to prevent unnecessary recursion
    stored_values = [[-1 for i in range(knapsack_weight+1)] for j in range(item_amount)]

    def recursion_search(item_index, knapsack_value, weight_remaining):
        """The core recursive function of the search
        
        Completes a depth-first search of the possible answers as a decision
        tree, but checks the stored_values cache to prevent unnecessary ¨
        computation. Branches are created by either adding or not adding
        a certain item to the knapsack. Each node recognises the index of its
        item, and the value and remaining weight of the knapsack at that state.
        """
        #stops branch of search if no more items
        if item_index == item_amount:
            return knapsack_value

        #checks if same state has already been computed
        if stored_values[item_index][weight_remaining] != -1:
            return stored_values[item_index][weight_remaining]
        
        #creates only "item not added branch" if item is too heavy
        item_weight = item_weights[item_index]
        if item_weight > weight_remaining:
            stored_values[item_index][weight_remaining] = recursion_search(item_index + 1, knapsack_value, weight_remaining)
            return stored_values[item_index][weight_remaining]
        
        #creates searches for item being added and not being added
        result_item_added = recursion_search(item_index + 1, knapsack_value, weight_remaining - item_weight) + item_values[item_index]
        result_item_excluded = recursion_search(item_index + 1, knapsack_value, weight_remaining)

        #saves results to memory and returns
        stored_values[item_index][weight_remaining] = max(result_item_added, result_item_excluded)
        return stored_values[item_index][weight_remaining]

    max_value = recursion_search(0, knapsack_value, knapsack_weight)
    end = datetime.now()
    time_difference = (end - start).total_seconds()

    return max_value, time_difference
        