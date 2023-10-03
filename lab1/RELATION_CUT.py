class RELATION_CUT:

    def __init__(self, size, data=None, type=None):
        self.size = size
        if type is None:
            self.data = data
        else:
            if type is None or type == 'empty' or size is None:
                self.data = dict()
            elif type == 'full':
                self.data = {i: {j for j in range(1, size + 1)} for i in range(1, size + 1)}
            elif type == 'diagonal':
                self.data = {i: {j for j in range(1, size + 1) if i==j} for i in range(1, size + 1)}
            elif type == 'antidiagonal':
                self.data = {i: {j for j in range(1, size + 1) if i!=j} for i in range(1, size + 1)}
            else:
                self.data = dict()
    
    def __str__(self):
        return str(self.data)
  
    def intersection(self, other):
        intersection={}
        for key in set(self.data.keys()).intersection(other.data.keys()):
            intersection[key] = self.data.get(key, set()).intersection(other.data.get(key, set()))
        return intersection

    

    def union(self, other):
        union = {}
        for key in set(self.data.keys()).union(other.data.keys()):
            union[key] = self.data.get(key, set()).union(other.data.get(key, set()))
        return union

    

    def difference(self, other):
        difference = {}
        for key in self.data.keys():
            difference[key] = self.data.get(key, set()).difference(other.data.get(key, set()))
        return difference



    def sym_diff(self, other):
        symmetric_difference = {}
        for key in self.data.keys():
            symmetric_difference[key] = self.data.get(key, set()).symmetric_difference(other.data.get(key, set()))
        return symmetric_difference

    
    def complement(self):
        complement = {}
        for i in range(1, self.size+1):
            complement[i] = {j for j in range(1,  self.size+1) if j not in self.data.get(i, set())}
        return complement

    
    def converce(self):
        converse = {}
        for i, related in self.data.items():
            for j in related:
                converse.setdefault(j, set()).add(i)
        return converse

    

    def dual(self):
        pass
    

    def composition(self, other):
        pass


# P = RELATION_MATR(size=4, data=[[1, 0, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [0, 0, 1, 1]])
# Q = RELATION_MATR(size=4, data=[[0, 0, 1, 1], [1, 1, 1, 0], [0, 1, 1, 1], [0, 1, 1, 0]]) 
P = {1: {1, 3}, 2: {2}, 3: {1, 2, 3, 4}, 4: {2, 3, 4}}
Q = {1: {2}, 2: {2, 3, 4}, 3: {1, 2, 3, 4}, 4: {1, 3}}
R = {1: {4}, 2: {3, 5}, 3: {4, 5}, 4: {1}, 5: {2, 4}}
print('Intersection\n', str(P.intersection(Q)))
print('\nUnion\n', str(P.union(Q)))
print('\nDifference\n', str(P.difference(Q)))
print('\nSymmetric difference\n', str(P.sym_diff(Q)))
print('\nComposition\n', str(P.composition(Q)))
print('\nComplement\n', str(P.complement()))
print('\nConverce\n', str(P.converce()))
print('\nDual\n', str(P.dual()))