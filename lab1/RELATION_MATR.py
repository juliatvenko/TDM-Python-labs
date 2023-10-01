import numpy as np
import itertools

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
            

    @staticmethod
    def get_intersection(P, Q):
        intersection = np.zeros((P.size, P.size), dtype=int)
        for x, y in itertools.product(range(P.size), range(P.size)):
            if P.data[x][y] == 1 and Q.data[x][y] == 1:
                intersection[x][y] = 1
        return RELATION_MATR(P.size, data=intersection)
    
    @staticmethod
    def get_union(P, Q):
        union = np.zeros((P.size, P.size), dtype=int)
        for x, y in itertools.product(range(P.size), range(P.size)):
            if P.data[x][y] == 1 or Q.data[x][y] == 1:
                union[x][y] = 1
        return RELATION_MATR(P.size, data=union)
    
    @staticmethod
    def get_difference(P, Q):
        difference = np.zeros((P.size, P.size), dtype=int)
        for x, y in itertools.product(range(P.size), range(P.size)):
            if P.data[x][y] == 1 and Q.data[x][y] == 0:
                difference[x][y] = 1
        return RELATION_MATR(P.size, data=difference)

    @staticmethod
    def get_sym_diff(P, Q):
        symmetric_difference = np.zeros((P.size, P.size), dtype=int)
        for x, y in itertools.product(range(P.size), range(P.size)):
            if (P.data[x][y] == 1 and Q.data[x][y] == 0) or \
                (P.data[x][y] == 0 and Q.data[x][y] == 1):
                symmetric_difference[x][y] = 1
        return RELATION_MATR(P.size, data=symmetric_difference)
    
    def get_complement(self):
        complement = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if self.data[x][y] == 0:
                complement[x][y] = 1
        return RELATION_MATR(self.size, data=complement)
    
    def get_converce(self):
        converce = np.zeros((self.size, self.size), dtype=int)
        for x, y in itertools.product(range(self.size), range(self.size)):
            if self.data[x][y] == 1:
                converce[y][x] = 1
        return RELATION_MATR(self.size, data=converce)
    

    def get_dual(self):
        return RELATION_MATR(self.size, self.get_complement().data).get_converce()
    
    @staticmethod
    def get_composition(P, Q):
        composition = np.zeros((P.size, P.size), dtype=int)
        for x, y, z in itertools.product(range(P.size), range(P.size), range(P.size)):
            if P.data[x][z] == 1 and Q.data[z][y] == 1:
                composition[x][y] = 1
        return RELATION_MATR(P.size, data=composition)


# P = RELATION_MATR(size=4, data=[[1, 0, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [0, 0, 1, 1]])
# Q = RELATION_MATR(size=4, data=[[0, 0, 1, 1], [1, 1, 1, 0], [0, 1, 1, 1], [0, 1, 1, 0]]) 
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
# print('Intersection\n', RELATION_MATR.get_intersection(P, Q).data)
# print('\nUnion\n', RELATION_MATR.get_union(P, Q).data)
# print('\nDifference\n', RELATION_MATR.get_difference(P, Q).data)
# print('\nSymmetric difference\n', RELATION_MATR.get_sym_diff(P, Q).data)
# print('\nComposition\n', RELATION_MATR.get_composition(P, Q).data)
# print('\nComplement\n', P.get_complement().data)
# print('\nConverce\n', P.get_converce().data)
# print('\nDual\n', P.get_dual().data)
# K = RELATION_MATR.get_difference(RELATION_MATR.get_composition(P, Q), R.get_dual())
# print('\nK = (P∘Q)\R^d\n', K.data)
# P = RELATION_MATR(size=4, type='full') 
# print(P.data)