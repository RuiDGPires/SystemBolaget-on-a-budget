from pulp import LpProblem, LpVariable, LpMaximize, LpStatusOptimal, PULP_CBC_CMD
from drink import Drink

def optimize(drinks, budget, verbose=False):
    prob = LpProblem("Alcohol_Purchase_Problem", LpMaximize)

    # Define the decision variables
    tmp = None
    cost_constraint = None
    vars = []
    for drink in drinks:
        x = LpVariable(drink.id(), lowBound=0, cat='Integer')

        # Define the objective function
        if tmp:
            tmp += drink.perc * drink.quantity * x
            cost_constraint +=  drink.getPrice() * x
        else:
            tmp = drink.perc * drink.quantity * x
            cost_constraint =  drink.getPrice() * x

        vars.append(x)

    prob += tmp
    # Define the cost constraint
    prob += cost_constraint <= budget

    # Solve the problem
    status = prob.solve(PULP_CBC_CMD(msg=verbose))

    res = []
    i = 0
    if status == LpStatusOptimal:
        for var in vars:
            if var.value():
                res.append((drinks[i], var.value()))
            i += 1
        return res
    else:
        assert False, "unkown"