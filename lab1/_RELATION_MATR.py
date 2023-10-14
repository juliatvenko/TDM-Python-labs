import numpy as np
import itertools
from memory_profiler import memory_usage
import time


class RELATION_MATR:

    def __init__(self, size, data=None, type=None):
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
        return self.intersection(self.converce()).data == set()
    
    def is_antysymmetric(self):
        return self.intersection(self.converce()).is_subset(\
            RELATION_MATR(size=self.size, type='diagonal'))

    def is_transitive(self):
        return self.composition(self).is_subset(self)

    def is_connected(self):
        return self.union(self.converce()).difference(RELATION_MATR(size=self.size, type='diagonal')).data \
              == RELATION_MATR(size=self.size, type='antidiagonal').data
    

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
        return RELATION_MATR(self.relations.intersection(self.converce().data))
    
 
    def asymmetric_part(self):
        return RELATION_MATR(self.relations.difference(self.symmetric_part().data))
    

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
 
# P = RELATION_MATR(size=4, data=[[1, 0, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [0, 0, 1, 1]])
# Q = RELATION_MATR(size=4, data=[[0, 0, 1, 1], [1, 1, 1, 0], [0, 1, 1, 1], [0, 1, 1, 0]]) 
P = RELATION_MATR(size=5, data=[[0, 0, 0, 1, 1], 
                                [1, 0, 1, 1, 0], 
                                [1, 0, 0, 0, 1], 
                                [0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0]])
Q = RELATION_MATR(size=5, data=[[0, 0, 0, 0, 0], 
                                [0, 0, 0, 0, 1], 
                                [0, 1, 0, 0, 1], 
                                [0, 1, 0, 0, 0],
                                [0, 0, 0, 1, 0]])
R = RELATION_MATR(size=5, data=[[0, 0, 0, 1, 0], 
                                [0, 0, 0, 0, 1], 
                                [0, 1, 0, 0, 0], 
                                [1, 0, 1, 0, 1],
                                [0, 1, 1, 0, 0]])
# print('Intersection\n', str(P.intersection(Q)))
# print('\nUnion\n', str(P.union(Q)))
# print('\nDifference\n', str(P.difference(Q)))
# print('\nSymmetric difference\n', str(P.sym_diff(Q)))
# print('\nComposition\n', str(P.composition(Q)))
# print('\nComplement\n', str(P.complement()))
# print('\nConverce\n', str(P.converce()))
# print('\nDual\n', str(P.dual()))

print("P: \n", str(P))
print("Q: \n", str(Q))
print("R: \n", str(R))

mem_usage_before = memory_usage(-1, interval=0.1, timeout=1)[0]
start_time = time.time()  

K = P.composition(Q).difference(R.dual())

end_time = time.time() 
mem_usage_after = memory_usage(-1, interval=0.1, timeout=1)[0]

K = P.composition(Q).difference(R.dual())
print('\nK = (P∘Q)\R^d\n', K.data)

print(f"Memory used: {mem_usage_after - mem_usage_before} MiB")
print(f"Time taken: {end_time - start_time} seconds")
# P = RELATION_MATR(size=4, type='full') 
# print(P.data)