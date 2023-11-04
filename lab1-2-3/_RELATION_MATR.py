from memory_profiler import memory_usage
import time
import numpy as np
import itertools
import networkx as nx
from _RELATION import RELATION
from RELATION_CUT import RELATION_CUT

class RELATION_MATR(RELATION):

    def __init__(self, size, data=None, type=None, relation_cut_obj=None):
        if isinstance(relation_cut_obj, RELATION_CUT):
            self.data = np.array(RELATION_MATR.dict2matrix(relation_cut_obj.data, relation_cut_obj.size))
            self.size = relation_cut_obj.size
        else:
            self.size = size
            if type is None:
                self.data = np.array(data, dtype=int)
            elif data is None:
                if type==None or type=='full':
                    self.data = np.ones((self.size, self.size), dtype=int)
                elif type=='empty':
                    self.data = np.zeros((self.size, self.size), dtype=int)
                elif type=='diagonal':
                    self.data = np.zeros((self.size, self.size), dtype=int)
                    np.fill_diagonal(self.data, 1)
                elif type=='antidiagonal':
                    self.data = np.ones((self.size, self.size), dtype=int) 
                    np.fill_diagonal(self.data, 0)
    
    def set2matrix(relations, size):
        matrix = np.zeros((size, size), dtype=int)
        for (i, j) in relations:
            matrix[i][j] = 1
        return matrix
    
    def dict2matrix(data, size):
        matrix = np.zeros((size, size), dtype=int)
        for col, rows in data.items():
            for row in rows:
                matrix[row-1][col-1] = 1
        return matrix 
        
    def __str__(self):
        return str(self.data)
  
    def intersection(self, other):
        intersection = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if self.data[x][y] == 1 and other.data[x][y] == 1:
                intersection[x][y] = 1
        return RELATION_MATR(self.size, data=intersection)
    

    def union(self, other):
        union = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if self.data[x][y] == 1 or other.data[x][y] == 1:
                union[x][y] = 1
        return RELATION_MATR(self.size, data=union)
    

    def difference(self, other):
        difference = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if self.data[x][y] == 1 and other.data[x][y] == 0:
                difference[x][y] = 1
        return RELATION_MATR(self.size, data=difference)


    def sym_diff(self, other):
        symmetric_difference = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if (self.data[x][y] == 1 and other.data[x][y] == 0) or \
                (self.data[x][y] == 0 and other.data[x][y] == 1):
                symmetric_difference[x][y] = 1
        return RELATION_MATR(self.size, data=symmetric_difference)
    
    def complement(self):
        complement = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if self.data[x][y] == 0:
                complement[x][y] = 1
        return RELATION_MATR(self.size, data=complement)
    
    def converce(self):
        converce = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if self.data[x][y] == 1:
                converce[y][x] = 1
        return RELATION_MATR(self.size, data=converce)
    

    def dual(self):
        return RELATION_MATR(self.size, self.complement().data).converce()
    

    def composition(self, other):
        composition = np.zeros((self.size, self.size), dtype=int)
        for x, y, z in itertools.product(range(self.size), range(self.size), range(self.size)):
            if self.data[x][z] == 1 and other.data[z][y] == 1:
                composition[x][y] = 1
        return RELATION_MATR(self.size, data=composition)

    def is_subset(self, other):
        for i in range(self.size):
            for j in range(self.size):
                if self.data[i][j] == 1 and other.data[i][j] == 0:
                    return False
        return True
    
    def is_reflexive(self):
        return RELATION_MATR(size=self.size, type='diagonal').is_subset(self)
    
    def is_antireflexive(self):
        return self.is_subset(RELATION_MATR(size=self.size, type='antidiagonal'))
    
    def is_symmetric(self):
        return self.is_subset(self.converce())

    def is_asymmetric(self):
        return np.array_equal(self.intersection(self.converce()).data, RELATION_MATR(size=self.size, type='empty').data)
    
    def is_antysymmetric(self):
        return self.intersection(self.converce()).is_subset(\
            RELATION_MATR(size=self.size, type='diagonal'))

    def is_transitive(self):
        return self.composition(self).is_subset(self)

    def is_connected(self):
        return np.array_equal(self.union(self.converce()).difference(RELATION_MATR(size=self.size, type='diagonal')).data, \
              RELATION_MATR(size=self.size, type='antidiagonal').data)
    

    def check_properties(self):
        return {
            'Reflexive': self.is_reflexive(),
            'Antireflexive': self.is_antireflexive(),
            'Symmetric': self.is_symmetric(),
            'Asymmetric': self.is_asymmetric(),
            'Antisymmetric': self.is_antysymmetric(),
            'Transitive': self.is_transitive(),
            'Acyclic': self.is_acyclic(),
            'Connected': self.is_connected()
        }
    
    def is_tolerant(self):
        return (self.is_reflexive()) and (self.is_symmetric())
    
    def is_equivalent(self):
        return (self.is_reflexive()) and (self.is_symmetric()) and (self.is_transitive())
    
    def is_quasiorder(self):
        return (self.is_reflexive()) and (self.is_transitive())
    
    def is_order(self):
        return (self.is_reflexive()) and (self.is_antysymmetric()) and (self.is_transitive())
    
    def is_strictorder(self):
        return (self.is_asymmetric()) and (self.is_transitive())
    
    def is_linearorder(self):
        return (self.is_reflexive()) and (self.is_antysymmetric()) \
            and (self.is_transitive()) and (self.is_connected()) 
    
    def is_strictlinearorder(self):
        return (self.is_reflexive()) and (self.is_antysymmetric()) \
            and (self.is_transitive()) and (self.is_connected()) and (self.is_asymmetric()) 
    
    def symmetric_part(self):
        return RELATION_MATR(self.size, self.intersection(RELATION_MATR(self.size, self.converce().data)).data)
    
 
    def asymmetric_part(self):
        return RELATION_MATR(self.size, self.difference(RELATION_MATR(self.size, self.symmetric_part().data)).data)
    

    def check_type(self):
        return {
            'Tolerant': self.is_tolerant(),
            'Equivalent': self.is_equivalent(),
            'Quasi order': self.is_quasiorder(),
            'Order': self.is_order(),
            'Strict order': self.is_strictorder(),
            'Linear order': self.is_linearorder(),
            'Strict linear order': self.is_strictlinearorder()
        }
    
    def is_acyclic(self):
        return nx.is_directed_acyclic_graph(nx.DiGraph(self.data))

    def transitive_closure(self):
        closure = self.data
        for k, i, j in itertools.product(range(self.size), range(self.size), range(self.size)):
            closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])
        return RELATION_MATR(self.size, closure)


    def reachability(self, start):
        return set(nx.single_source_shortest_path_length(self.graph, start).keys())

    def is_mutually_reachable(self, a, b):
        return (b in self.reachability(a)) and (a in self.reachability(b))
    
    def get_equivalence_classes(self):
        equivalence_classes = []
        visited = set()

        P_trans_sym = self.transitive_closure().symmetric_part().data

        for i in range(self.size):
            if i not in visited:
                eq_class = {i}
                for j in range(self.size):
                    if P_trans_sym[i][j] and P_trans_sym[j][i]:
                        eq_class.add(j)
                        visited.add(j)
                equivalence_classes.append(eq_class)
        return equivalence_classes
    
    def factorized(self):
        equivalence_classes = self.get_equivalence_classes()
        PD = [[0] * len(equivalence_classes) for _ in range(len(equivalence_classes))]
        
        for i, class_i in enumerate(equivalence_classes):
            for j, class_j in enumerate(equivalence_classes):
                for x in class_i:
                    for y in class_j:
                        if self.data[x][y] == 1:
                            PD[i][j] = 1
                            break  
                    if PD[i][j] == 1:
                        break  
        return RELATION_MATR(len(equivalence_classes), PD)
    
    def relation_ranged(self):
        Pm = np.zeros((self.size, self.size), dtype=int)
        for i, j in itertools.product(range(self.size), repeat=2):
            Pm[i][j] = self.data[i][j] - self.data[j][i]
        return Pm
    
    def calculate_distance(self, other):
        def find_equivalence_classes(matrix):
            num_elements = matrix.shape[0]
            classes = []
            for i in range(num_elements):
                if not any(i in equivalence_class for equivalence_class in classes):
                    new_class = {j for j in range(num_elements) if matrix[i, j] == 1}
                    classes.append(new_class)
            return classes

        def get_intersection_classes(classes1, classes2):
            intersection = []
            for class1 in classes1:
                for class2 in classes2:
                    inter = class1.intersection(class2)
                    if inter not in intersection and inter:
                        intersection.append(inter)
            return intersection

        def calculate_r_values(equivalence_classes, intersection_classes):
            r_values = []
            for eq_cls in equivalence_classes:
                intersections = [eq_cls.intersection(inter_class) for inter_class in intersection_classes\
                                  if eq_cls.intersection(inter_class)]
                r_values.append(len(intersections))
            return r_values

        def calculate_max_inter_sizes(equivalence_classes, intersection_classes):
            max_intersection_size = []
            for eq_cls in equivalence_classes:
                intersections = [eq_cls.intersection(inter_class) for inter_class in intersection_classes\
                                  if eq_cls.intersection(inter_class)]
                max_intersection_size.append(max(len(inter_class) for inter_class in intersections))
            return max_intersection_size
        
        if not self.is_equivalent() and other.is_equivalent():
            raise TypeError('Matixes not equivalent')
        
        eq_classes_P = find_equivalence_classes(self.data)
        eq_classes_R = find_equivalence_classes(other.data)
        classes_intersection = get_intersection_classes(eq_classes_P, eq_classes_R)
        r_P = calculate_r_values(eq_classes_P, classes_intersection)
        r_R = calculate_r_values(eq_classes_R, classes_intersection)
        P_inter_max_sizes = calculate_max_inter_sizes(eq_classes_P, classes_intersection)
        R_inter_max_sizes = calculate_max_inter_sizes(eq_classes_R, classes_intersection)

        distance = 0
        for i in range(len(r_P)):
            distance += 2 * (abs(len(eq_classes_P[i]))  - abs(P_inter_max_sizes[i])) - r_P[i] + 1
        for i in range(len(r_R)):
            distance += 2 * (abs(len(eq_classes_R[i])) - abs(R_inter_max_sizes[i])) - r_R[i] + 1
        return distance
    
    def get_distance(self, other):
        return np.abs(self.relation_ranged() - other.relation_ranged()).sum()/2
 
#######################################LAB1###########################################
# P = RELATION_MATR(size=5, data=[[0, 0, 0, 1, 1], 
#                                 [1, 0, 1, 1, 0], 
#                                 [1, 0, 0, 0, 1], 
#                                 [0, 0, 1, 0, 0],
#                                 [0, 0, 0, 0, 0]])
# Q = RELATION_MATR(size=5, data=[[0, 0, 0, 0, 0], 
#                                 [0, 0, 0, 0, 1], 
#                                 [0, 1, 0, 0, 1], 
#                                 [0, 1, 0, 0, 0],
#                                 [0, 0, 0, 1, 0]])
# R = RELATION_MATR(size=5, data=[[0, 0, 0, 1, 0], 
#                                 [0, 0, 0, 0, 1], 
#                                 [0, 1, 0, 0, 0], 
#                                 [1, 0, 1, 0, 1],
#                                 [0, 1, 1, 0, 0]])
# print('Intersection\n', str(P.intersection(Q)))
# print('\nUnion\n', str(P.union(Q)))
# print('\nDifference\n', str(P.difference(Q)))
# print('\nSymmetric difference\n', str(P.sym_diff(Q)))
# print('\nComposition\n', str(P.composition(Q)))
# print('\nComplement\n', str(P.complement()))
# print('\nConverce\n', str(P.converce()))
# print('\nDual\n', str(P.dual()))

# print("P: \n", str(P))
# print("Q: \n", str(Q))
# print("R: \n", str(R))

# mem_usage_before = memory_usage(-1, interval=0.1, timeout=1)[0]
# start_time = time.time()  

# K = P.composition(Q).difference(R.dual())

# end_time = time.time() 
# mem_usage_after = memory_usage(-1, interval=0.1, timeout=1)[0]

# K = P.composition(Q).difference(R.dual())
# print('\nK = (P∘Q)\R^d\n', K.data)

# print(f"Memory used: {mem_usage_after - mem_usage_before} MiB")
# print(f"Time taken: {end_time - start_time} seconds")

#######################################LAB2###########################################
# P = RELATION_MATR(size=5, data=[[0, 0, 0, 1, 1], 
#                                 [1, 0, 1, 1, 0], 
#                                 [1, 0, 0, 0, 1], 
#                                 [0, 0, 1, 0, 0],
#                                 [0, 0, 0, 0, 0]])
# Q = RELATION_MATR(size=5, data=[[0, 0, 0, 0, 0], 
#                                 [0, 0, 0, 0, 1], 
#                                 [0, 1, 0, 0, 1], 
#                                 [0, 1, 0, 0, 0],
#                                 [0, 0, 0, 1, 0]])

# print('Is Q transitive:', Q.is_transitive())
# if not Q.is_transitive():
#     print('Q transitive closure\n'+str(Q.transitive_closure()))
#     print('Is Q transitive closure transitive:', Q.transitive_closure().is_transitive())

# print('\nP factorized\n', P.factorized())

# print('\nP factorized properties\n' + "\n".join(f"{prop}: {val}" for prop, val in P.factorized().check_properties().items()))
# print('\nP factorized type\n' + "\n".join(f"{prop}: {val}" for prop, val in P.factorized().check_type().items()))

#######################################LAB5###########################################
#####################################EXAMPLE##########################################
# P1 = RELATION_MATR(size=12, data=[[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#                                   [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#                                   [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#                                   [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#                                   [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
#                                   [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
#                                   [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
#                                   [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
#                                   [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
#                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
#                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]])

# P2 = RELATION_MATR(size=12, data=[[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
#                                   [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#                                   [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#                                   [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#                                   [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
#                                   [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#                                   [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#                                   [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
#                                   [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
#                                   [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
#                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
# print(Distance between P1 and P2:', P1.calculate_distance(P2))

#####################################TASK##########################################
R_relation_cut = RELATION_CUT(data={1: {1, 2}, 
                                    2: {2, 5}, 
                                    3: {3, 5}, 
                                    4: {4}, 
                                    5: {5}})
R=RELATION_MATR(relation_cut_obj=R_relation_cut, size=5)
G=RELATION_MATR(size=5, data=[[1, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0],
                               [1, 1, 1, 1, 1],
                               [1, 1, 0, 1, 1],
                               [0, 0, 0, 0, 1]])
print('R: '+str(R_relation_cut))
print('G:\n'+str(G))
print('Distance between G and R:', G.get_distance(R))


Q1=RELATION_MATR(size=5, data=[[1, 0, 0, 0, 1],
                               [0, 1, 0, 0, 0],
                               [0, 0, 1, 1, 0],
                               [0, 0, 1, 1, 0],
                               [1, 0, 0, 0, 1]])
                         
Q2=RELATION_MATR(size=5, data=[[1, 0, 0, 0, 1],
                               [0, 1, 0, 1, 0],
                               [0, 0, 1, 0, 0],
                               [0, 1, 0, 1, 0],
                               [1, 0, 0, 0, 1]])
print('Q1:\n'+str(Q1))
print('Q2:\n'+str(Q2))
print('Is Q1 equivalent:', Q1.is_equivalent())
print('Is Q2 equivalent:', Q2.is_equivalent())
print('Distance between Q1 and Q2:', Q1.calculate_distance(Q2))