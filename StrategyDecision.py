import numpy as np
import itertools

class StrategyDecision:
    def __init__(self, payment_matrix, probabilities):
        self.payment_matrix = payment_matrix
        self.probabilities = probabilities

    def criterion_bayes_laplace(self):
        return(np.argmax([np.dot(strategy, self.probabilities) for strategy in self.payment_matrix])+1)
    
    def criterion_minmax(self):
        return(np.argmax([min(strategy) for strategy in self.payment_matrix]) + 1)
    
    def criterion_maxmin(self):
        return(np.argmin([max(strategy) for strategy in np.max(self.payment_matrix, axis=0) - self.payment_matrix]) + 1)
    
    def criterion_hurwitz(self, alpha):
        return(np.argmax([alpha * min(strategy) + (1 - alpha) * max(strategy) for strategy in self.payment_matrix]) + 1)
    
    def decision_strategy(self):
        print('Bayes-Laplace criteria:', self.criterion_bayes_laplace())
        print('Wald criteria:', self.criterion_minmax())
        print('Savage criteria:', self.criterion_maxmin())
        for alpha in [0, 0.2, 0.4, 0.8]:
            print('Hurwitz criteria for alpha='+str(alpha)+': '+str(self.criterion_hurwitz(alpha)))

def get_payment_matrix_task1(cost, price, transportation, demand):
    profit = price - cost - transportation
    payment_matrix = np.zeros((len(demand), len(demand)), dtype=int)
    for i, j in itertools.product(range(len(demand)), range(len(demand))):
        if demand[i] > demand[j]:
            payment_matrix[i][j] = demand[j]*profit - (demand[i] - demand[j])*profit
        else:
            payment_matrix[i][j] = demand[i]*profit
    return payment_matrix

    
def get_payment_matrix_task2(distance, base_cost, production_costs, supply_party, hi_values, loss_day_late):
    payment_matrix = np.zeros((len(supply_party), len(production_costs)), dtype=int)
    for i, j in itertools.product(range(len(supply_party)), range(len(production_costs))):
        payment_matrix[i][j] = supply_party[i]*(production_costs[j] - base_cost) - \
                               hi_values[i]*distance-j*loss_day_late
    return payment_matrix

A1 = 260
A2 = 500
C = 5
B1, B2, B3, B4, B5 = 55, 65, 75, 85, 95
P1, P2, P3, P4, P5 = 0.15, 0.2, 0.2, 0.3, 0.15

payment_matrix_task1 = get_payment_matrix_task1 (
cost = A1,
price = A2,
transportation = C,
demand = [B1, B2, B3, B4, B5]
)
print('Task 1 payment matrix:\n'+str(payment_matrix_task1))
print('\nTask 1 best strategies:')
StrategyDecision(
    payment_matrix = payment_matrix_task1,
    probabilities = [P1, P2, P3, P4, P5]
).decision_strategy()

D = 520
C = 120
C1, C2, C3, C4, C5 = 220, 200, 190, 170, 160
A1, A2, A3, A4, A5 = 12, 16, 20, 24, 28
H1, H2, H3 = 0.9, 1.0, 1.5
B = 55
p1, p2, p3, p4, p5 = 0.3, 0.25, 0.2, 0.15, 0.1

payment_matrix_task2 = get_payment_matrix_task2 (
production_costs = [C1, C2, C3, C4, C5],
hi_values = [H1, H2, H2, H2, H3],
base_cost = C,
supply_party = [A1, A2, A3, A4, A5],
loss_day_late = B,
distance = D,
)
print('\n\nTask 2 payment matrix:\n'+str(payment_matrix_task2))
print('\nTask 2 best strategies:')
StrategyDecision(
    payment_matrix = payment_matrix_task2,
    probabilities = [p1, p2, p3, p4, p5]
).decision_strategy()