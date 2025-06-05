from datetime import datetime


def b_knapsack_solver(item_weights, item_values, knapsack_weight):
    """Solves a knapsack problem using brute-force, returns answer and time taken

    Items are represented through two lists: the weights and values.
    """

    start = datetime.now()

    knapsack_value = 0
    item_amount = len(item_weights)

    def recursion_search(item_index, knapsack_value, weight_remaining):
        """The core recursive function of the brute-force search
        
        Completes a depth-first search of the possible answers as a decision
        tree. Branches are created by either adding or not adding
        a certain item to the knapsack. Each node recognises the index of its
        item, and the value and remaining weight of the knapsack at that state.
        """

        #stops branch of search if no more items
        if item_index == item_amount:
            return knapsack_value

        #creates only "item not added" search if item is too heavy
        item_weight = item_weights[item_index]
        if item_weight > weight_remaining:
            return recursion_search(item_index+1, knapsack_value, weight_remaining)

        #creates search for item being added and not added
        result_when_in = recursion_search(item_index+1, knapsack_value + item_values[item_index], weight_remaining - item_weight)
        result_when_out = recursion_search(item_index+1, knapsack_value, weight_remaining)

        return max(result_when_in, result_when_out)

    max_value = recursion_search(0, knapsack_value, knapsack_weight)
    end = datetime.now()
    time_difference = (end - start).total_seconds()

    return max_value, time_difference