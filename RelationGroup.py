import numpy as np 
from collections import Counter
import itertools

class RelationGroup:

    def __init__(self, P_group):
        self.P_group = P_group
        self.expert_alternative = np.hstack([np.sum(P, axis=1)[:, np.newaxis] for P in self.P_group])
        self.num_alternatives, self.num_experts = self.expert_alternative.shape

    def __str__(self):
        headers = [f"E{i+1}" for i in range(self.num_experts)]
        row_labels = [f"x{i+1}" for i in range(self.num_alternatives)]
        expert_alternative_str = "Scored by each expert alternatives:\n"
        expert_alternative_str += '    '+'  '.join(headers) + "\n"
        for label, row in zip(row_labels, self.expert_alternative):
            expert_alternative_str += f'{label:2}' + ' '.join(f'{num:3}' for num in row) + "\n"
        return expert_alternative_str
    
    def get_expert_alternative_score(self):
        return np.hstack([np.sum(P, axis=1)[:, np.newaxis] for P in self.P_group])
    
    def get_place_expert_alternative(self):
        return np.hstack([(np.argsort(-np.sum(P, axis=1)) + 1)[:, np.newaxis] for P in self.P_group])

    def get_preference_matrix(self):
        S = np.zeros((self.num_alternatives, self.num_experts), dtype=int)
        
        for i, j, k in itertools.product(range(self.num_alternatives), repeat=3):
            S[i, j] += (self.expert_alternative[i, k] > self.expert_alternative[j, k])
        return S

    def get_relation_matrix(S):
        num_alternatives, num_experts = S.shape
        P = np.zeros((num_alternatives, num_experts), dtype=int)
        for i, j in itertools.product(range(num_alternatives), range(num_experts)):
            P[i][j] = (i != j and S[i, j] - S[j, i] >= 0) 
        return P   
    
    def decide_most_votes(self):
        print("\tMOST VOTES PRINCIPLE")

        place_expert_alternative = self.get_place_expert_alternative()
        headers = [f"E{i+1}" for i in range(self.num_experts)]
        row_labels = [f"{i+1}" for i in range(self.num_alternatives)]
        print("Ranged by each expert alternatives:")
        print('    ', '  '.join(headers))
        for label, row in zip(row_labels, place_expert_alternative):
            print(f'{label:4}', '  '.join(f'x{num}' for num in row))
        
        print("\n", end="")
        place = 1
        for alternative, votes in sorted(Counter(place_expert_alternative[0]).items(), key=lambda x: -x[1]):
            if votes == 1:
                print(f"Place {place}: alternative x{alternative} ({votes} vote)")
            else:
                print(f"Place {place}: alternative x{alternative} ({votes} votes)")
            place += 1
    

    def decide_kondorce(self):
        print("\n\tKONDORCE PRINCIPLE")
        S = self.get_preference_matrix()
        P = RelationGroup.get_relation_matrix(S)

        print("Preference matrix S:\n"+str(S))
        print("Resulting relation matrix P:\n"+str(P))
        print("\n", end="")

        ranking = np.argsort(-P.sum(axis=1)) + 1  
        for rank, alternative in enumerate(ranking, start=1):
            print(f"Place {rank}: alternative x{alternative}")
    
    def decide_borda(self):
        print("\n\tBORDA PRINCIPLE")
        borda_scores = np.sum(self.expert_alternative, axis=1)

        sorted_indices = np.argsort(-borda_scores)
        
        places = {}
        current_place = 1
        current_score = borda_scores[sorted_indices[0]]
        for index in sorted_indices:
            if borda_scores[index] == current_score:
                places[f"x{index+1}"] = current_place
            else:
                current_place += 1
                current_score = borda_scores[index]
                places[f"x{index+1}"] = current_place

        places =  {alternative: place for alternative, place in sorted(places.items(), \
                                                                       key=lambda item: item[1])}
        for alternative, place in places.items():
            print(f"Place {place}: {alternative} ({borda_scores[int(alternative[1:])-1]} votes)")
    
    def median_kemeni(self):
        print("\n\tMEDIAN KEMENI")
        relation = np.zeros((self.num_alternatives, self.num_experts), dtype=int)

        for i in range(self.num_alternatives):
            for j in range(i, self.num_experts):
                for P in self.P_group:
                    if P[i][j] > P[j][i]:
                        P[i][j], P[j][i] = 1, -1
                    elif P[i][j] < P[j][i]:
                        P[i][j], P[j][i] = -1, 1
                    else:
                        P[i][j] = P[j][i] = 0

        print("Matrix of losses R:")

        for i in range(self.num_alternatives):
            for j in range(self.num_experts):
                if i != j:
                    relation[i][j] = sum(1 - P[i][j] for P in self.P_group)
        print(relation)
        print("\nRanging of alternatives: ", end='')
        ranking = []

        for _ in range(self.num_alternatives):
            costs = [sum(relation[i]) if i not in ranking else float('inf') for i in range(self.num_experts)]
            min_index = costs.index(min(costs))
            ranking.append(min_index)
        print(' '.join(str(r + 1) for r in ranking))

        distance = sum(relation[ranking[i]][ranking[j]] for i in range(len(ranking)) for j in range(i + 1, len(ranking)))
        print(f"Distance: {distance}")

        print("Checked ranging of alternatives: ", end='')
        for i in range(len(ranking) - 1):
            if relation[ranking[i]][ranking[i + 1]] >= relation[ranking[i + 1]][ranking[i]]:
                ranking[i], ranking[i + 1] = ranking[i + 1], ranking[i]

        print(' '.join(str(r + 1) for r in ranking))
        return distance
  


P1 = np.array([[0, 0, 0, 0, 0],
               [1, 0, 0, 1, 1],
               [1, 1, 0, 1, 1],
               [1, 0, 0, 0, 0],
               [1, 0, 0, 1, 0]])

P2 = np.array([[0, 1, 1, 1, 0],
               [0, 0, 1, 1, 0],
               [0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0],
               [1, 1, 1, 1, 0]])

P3 = np.array([[0, 1, 1, 0, 1],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0],
               [1, 1, 1, 0, 1],
               [0, 1, 1, 0, 0]])

P4 = np.array([[0, 1, 1, 1, 1],
               [0, 0, 0, 1, 0],
               [0, 1, 0, 1, 1],
               [0, 0, 0, 0, 0],
               [0, 1, 0, 1, 0]])

P5 = np.array([[0, 1, 1, 0, 1],
               [0, 0, 0, 0, 0],
               [0, 1, 0, 0, 1],
               [1, 1, 1, 0, 1],
               [0, 1, 0, 0, 0]])
P_group = RelationGroup(P_group=[P1, P2, P3, P4, P5])

print(str(P_group))
P_group.decide_most_votes()
P_group.decide_kondorce()
P_group.decide_borda()
P_group.median_kemeni()