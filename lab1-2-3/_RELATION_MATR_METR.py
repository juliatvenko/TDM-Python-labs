import numpy as np
import itertools
from math import sqrt
from _RELATION_MATR import RELATION_MATR

class RELATION_MATR_METR(RELATION_MATR):

    def __init__(self, data):
        self.data = np.array(data, dtype=float)
        self.size = self.data.shape[0]
    
    def __str__(self):
        return str(self.data)
    
    def set_v(self, i, j, value):
        self.data[i][j]=value
    
    def get_v(self, i, j):
        return self.data[i][j]
    
    def is_additive(self):
        for i, j, k in itertools.product(range(self.size), range(self.size), range(self.size)):
            if self.data[i][k] !=0 and self.data[k][j]!=0:
                if self.data[i][j]!=0 and self.data[i][j] != self.data[i][k] + self.data[k][j]:
                    return False
        return True

    def is_multiplicative(self):
        for i, j, k in itertools.product(range(self.size), range(self.size), range(self.size)):
            if self.data[i][k]!=0 and self.data[k][j]!=0:
                if self.data[i][j]!=0 and self.data[i][j] != self.data[i][k] * self.data[k][j]:
                    return False
        return True
    
    def is_consistent(self):
        for i, j in itertools.product(range(self.size), range(self.size)):
            if self.data[i][j] != -self.data[j][i]:
                return False
        return True
    
    def is_additively_transitive(self):
        for i, j, k in itertools.product(range(self.size), range(self.size), range(self.size)):
            if self.data[i][j] != self.data[i][k] + self.data[k][j]:
                    return False
        return True

    def is_multiplicatively_transitive(self):
        for i, j, k in itertools.product(range(self.size), range(self.size), range(self.size)):
            if self.data[i][j] != self.data[i][k] * self.data[k][j]:
                    return False
        return True
    
    def check_properties(self):
        properties_dict = {
            'Additive': self.is_additive(),
            'Multiplicative': self.is_multiplicative(),
            'Consistent': self.is_consistent(),
            'Additively transitive': self.is_additively_transitive(),
            'Multiplicatively transitive': self.is_multiplicatively_transitive()
        }

        return "\n".join(f"{prop}: {val}" for prop, val in properties_dict.items())
    
    def union(self, other):
        union = np.zeros((self.size, other.size), dtype=float)
        for i, j in itertools.product(range(self.size), range(other.size)):
            if self.data[i][j] == 0 and other.data[i][j] != 0:
                union[i][j] = other.data[i][j]
            elif self.data[i][j] != 0 and other.data[i][j] == 0:
                union[i][j] = self.data[i][j]
            elif self.is_additive():
                union[i][j] = (self.data[i][j] + other.data[i][j])/2
            elif self.is_multiplicative():
                union[i][j] = round(sqrt(self.data[i][j] * other.data[i][j]), 2)
        return RELATION_MATR_METR(data=union)
    
    def intersection(self, other):
        intersection = np.zeros((self.size, other.size), dtype=float)
        for i, j in itertools.product(range(self.size), range(other.size)):
            if self.data[i][j] != 0 and other.data[i][j] != 0:
                if self.is_additive():
                    intersection[i][j] = (self.data[i][j] + other.data[i][j]) / 2
                elif self.is_multiplicative():
                    intersection[i][j] = round(sqrt(self.data[i][j] * other.data[i][j]), 2)
        return RELATION_MATR_METR(data=intersection)

    def difference(self, other):
        difference = np.zeros((self.size, other.size), dtype=float)
        for i, j in itertools.product(range(self.size), range(other.size)):
            if self.data[i][j] != 0 and other.data[i][j] == 0:
                difference[i][j] = self.data[i][j]
        return RELATION_MATR_METR(data=difference)

    def composition(self, other):
        composition = np.zeros((self.size, other.size), dtype=float)
        for i, j in itertools.product(range(self.size), range(other.size)):
            K = [k for k in range(self.size) if self.data[i][k] != 0 and other.data[k][j] != 0]
            if not K:  
                continue
            if self.is_additive():
                composition[i][j] = sum(self.data[i][k] + other.data[k][j] for k in K) / len(K)
            elif self.is_multiplicative():
                composition[i][j] = round((np.prod([self.data[i][k] * other.data[k][j] for k in K]))**(1/len(K)), 2)
        return RELATION_MATR_METR(data=composition)

#################################EXAMPLE###################################################    
# Additive metrized relations
P = RELATION_MATR_METR(data=np.array([[0, 0, 0, 5, 0],
                                      [2, 0, 0, 7, 1],
                                      [4, 2, 0, 9, 3],
                                      [0, 0, 0, 0, 0],
                                      [1, 0, 0, 6, 0]]))

Q = RELATION_MATR_METR(data=np.array([[0, 0, 0, 0, 0],
                                      [5, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0],
                                      [4, 0, 0, 0, 0],
                                      [7, 2, 0, 3, 0]]))
print('P properties\n'+P.check_properties())
print('Q properties\n'+Q.check_properties())
print('P and Q union\n'+ str(P.union(Q)))
print('P and Q intersection\n'+ str(P.intersection(Q)))
print('P and Q difference\n'+ str(P.difference(Q)))
print('P and Q composition\n'+ str(P.composition(Q)))

# Multiplicative metrized relations
P1 = RELATION_MATR_METR(data=np.array([[1, 3, 6, 6, 12],
                                      [0, 1, 2, 2, 4],
                                      [0, 0, 1, 1, 2],
                                      [0, 0, 1, 1, 2],
                                      [0, 0, 0, 0, 1]]))

Q1 = RELATION_MATR_METR(data= np.array([[1, 0, 0, 2, 10],
                                       [0, 1, 0, 0, 0],
                                       [0, 0, 1, 0, 6],
                                       [0, 0, 0, 1, 5],
                                       [0, 0, 0, 0, 1]])) 

print('P1 properties\n'+P1.check_properties())
print('Q1 properties\n'+Q1.check_properties())
print('P1 and Q1 union\n'+ str(P1.union(Q1)))
print('P1 and Q1 intersection\n'+ str(P1.intersection(Q1)))
print('P1 and Q1 difference\n'+ str(P1.difference(Q1)))
print('P1 and Q1 composition\n'+ str(P1.composition(Q1))) 