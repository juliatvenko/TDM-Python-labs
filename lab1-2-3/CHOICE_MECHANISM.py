import itertools
import numpy as np

class ChoiceMechanism:
    def __init__(self, Q, QE, order, main_criteria, QM, alpha=None, lambda_vector=None):
        self.Q = Q
        self.num_alternatives = Q.shape[0]
        self.num_criteria = Q.shape[1]
        self.alpha = alpha
        self.QE = QE
        self.lambda_vector = lambda_vector
        self.order = order
        self.main_criteria = main_criteria
        self.QM = QM

    def search_max(T):
        return np.where(np.all(T == 1, axis=1))[0]

    def search_min(T):
        return np.where(np.all(T == 1, axis=0))[0]

    def search_majr(T):
        return np.where(np.all(T == 0, axis=0))[0]

    def search_minr(T):
        return np.where(np.all(T == 0, axis=1))[0]
    
    def format_alternatives(lst):
        if len(lst) == 0:
            return 'nothing found'
        else:
            return ", ".join(f"a{i + 1}" for i in lst)
    
    def set_mechanism(self, mechanism):
        if mechanism == "pareto":
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.pareto_decision()))
            print('Majorants: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_majr(self.pareto_decision()))))
        elif mechanism == "slater":
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.slater_decision()))
            print('Maximums: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_max(self.slater_decision()))))
        elif mechanism == "best result":
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.best_result_decision()))
            print('Maximums: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_max(self.best_result_decision()))))
        elif mechanism == "guaranteed result":
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.guaranteed_result_decision()))
            print('Maximums: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_max(self.guaranteed_result_decision()))))
        elif mechanism == "gurvitz":
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.gurvitz_criterion_decision() ))
            print('Maximums: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_max(self.gurvitz_criterion_decision())))) 
        elif mechanism == "standard": 
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.by_standard_decision()))
            print('Maximums: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_max(self.by_standard_decision()))))
        elif mechanism == "criteria aggregation":
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.criteria_aggregation_decision()))
            print('Maximums: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_max(self.criteria_aggregation_decision())))) 
        elif mechanism == "lexicographical":
            print(f"\n{mechanism.upper()} decision T matrix\n" + str(self.lexicographical_order_decision()))
            print('Majorants: '+ str(ChoiceMechanism.format_alternatives(ChoiceMechanism.search_majr(self.lexicographical_order_decision()))))
        elif mechanism == "main criteria":
            T = self.main_criteria_decision()
            Tc = T[np.any(T, axis=1)][:, np.any(T, axis=0)]
            print(f"\n{mechanism.upper()} decision Tc matrix\n" + str(Tc))
            print('Maximums: '+ str(ChoiceMechanism.format_alternatives(np.arange(T.shape[0])[np.any(T, axis=1)][ChoiceMechanism.search_max(Tc)])))
        else:
            raise ValueError(f"Unknown mechanism: {mechanism}")

    def pareto_decision(self):
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
                if i != j:
                    difference = self.Q[i] - self.Q[j] 
                    if np.all(difference >= 0) and np.any(difference > 0):
                        T[i][j] = 1
        return T
    
    
    def slater_decision(self):
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
                if i != j:
                    difference = self.Q[i] - self.Q[j] 
                    if np.all(difference > 0):
                        T[i][j] = 1
                else:
                    T[i][j] = 1
        return T
    
    def best_result_decision(self):
        max_values = np.max(self.Q, axis=1)
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
            if max_values[i] >= max_values[j]:
                T[i][j] = 1        
        return T
    
    def guaranteed_result_decision(self):
        min_values = np.min(self.Q, axis=1)
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
            if min_values[i] >= min_values[j]:
                T[i][j] = 1    
        return T
    
    def gurvitz_criterion_decision(self):
        min_values = np.min(self.Q, axis=1)
        max_values = np.max(self.Q, axis=1)
        gurvitz_values = self.alpha * min_values + (1 - self.alpha) * max_values
        T = np.zeros((self.num_criteria, self.num_criteria), dtype=int)
        for i, j in itertools.product(range(self.num_criteria), repeat=2):
                if gurvitz_values[i] > gurvitz_values[j]:
                    T[i][j] = 1
        return T
    
    def by_standard_decision(self):
        deviations = np.abs(self.Q - self.QE).sum(axis=1)
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
            if deviations[i] <= deviations[j]:
                    T[i][j] = 1     
        return T
    
    def criteria_aggregation_decision(self):
        aggregate_scores = self.Q.dot(self.lambda_vector)
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
                T[i][j] = int(aggregate_scores[i] >= aggregate_scores[j]) 
        return T
    
    def lexicographical_order_decision(self):
        self.Q = self.Q[:, [int(item[1:])-1 for item in self.order.split("->")]]
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
            for k in range(self.num_criteria):
                if self.Q[i][k] > self.Q[j][k]:
                    T[i][j] = 1
                    break
                elif self.Q[i][k] < self.Q[j][k]:
                    break         
        return T
    
    def main_criteria_decision(self):
        T = np.zeros((self.num_alternatives, self.num_alternatives), dtype=int)
        self.QM = np.insert(self.QM, self.main_criteria-1, 0)
        for i, j in itertools.product(range(self.num_alternatives), repeat=2):
            if i == j:
                if all([self.Q[i][k] >= self.QM[k] for k in range(self.num_criteria)]):
                    T[i][j] = 1
            else:
                if all(self.Q[t, k] >= self.QM[k] for t in [i, j] for k in range(self.num_criteria)):
                    if self.Q[i][self.main_criteria - 1] >= self.Q[j][self.main_criteria - 1]:
                        T[i][j] = 1          
        return T
    

Q = ChoiceMechanism(Q=np.array([[1, 3, 6],
                                [2, 5, 4],
                                [2, 4, 6],
                                [3, 2, 5]]),
                    QE=np.array([2, 3, 5]),
                    order="Q1->Q2->Q3",
                    main_criteria=1,
                    QM=np.array([3, 4])
                    )
Q.set_mechanism(mechanism="pareto")
Q.set_mechanism(mechanism="slater")
Q.set_mechanism(mechanism="best result")
Q.set_mechanism(mechanism="guaranteed result")
Q.set_mechanism(mechanism="standard")
Q.set_mechanism(mechanism="lexicographical")
Q.set_mechanism(mechanism="main criteria")

    

    


