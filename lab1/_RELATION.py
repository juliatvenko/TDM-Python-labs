from abc import ABC, abstractmethod

class RELATION(ABC):
    def __init__(self, relations=None, size=None, type=None): 
        self.size = size
        if relations is not None:
            self.relations = relations
            if size is None:
                self.size = max(max(pair) for pair in self.relations) + 1
        else:
            if type is None or type == 'empty' or size is None:
                self.relations = set()
            elif type == 'full':
                self.relations = {(i, j) for i in range(size) for j in range(size)}
            elif type == 'diagonal':
                self.relations = {(i, i) for i in range(size)}
            elif type == 'antidiagonal':
                self.relations = {(i, j) for i in range(size) for j in range(size) if i != j}
            else:
                self.relations = set()

    def __str__(self):
        return "{" + "\n".join(f"({x}, {y})" for x, y in sorted(self.relations)) + "}"
    
    @abstractmethod
    def intersection(self, other):
        return RELATION(sorted(self.relations.intersection(other.relations)))

    @abstractmethod
    def union(self, other):
        return RELATION(sorted(self.relations.union(other.relations)))
    
    @abstractmethod
    def difference(self, other):
        return RELATION(sorted(self.relations.difference(other.relations)))
    
    @abstractmethod
    def sym_diff(self, other):
        return RELATION(sorted(self.relations.symmetric_difference(other.relations)))

    @abstractmethod
    def complement(self):
        return RELATION(RELATION(size=self.size, type='full').relations - self.relations)
    
    @abstractmethod
    def converce(self):
        return RELATION(sorted({(y, x) for (x, y) in self.relations}))
    
    @abstractmethod
    def composition(self, other):
        return RELATION(sorted({(x, y) for x, z1 in self.relations for z2, y in other.relations if z1 == z2}))
    
    @abstractmethod
    def dual(self):
        return RELATION(RELATION(self.complement().relations).relations).converce()


P = RELATION(relations={(0, 0), (0, 2), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3), (3, 2), (3, 3)})
Q = RELATION(relations={(0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2)})


print('Intersection\n', P.intersection(Q))
print('\nUnion\n', P.union(Q))
print('\nDifference\n', P.difference(Q))
print('\nSymmetric difference\n', P.sym_diff(Q))
print('\nComposition\n', P.composition(Q))
print('\nComplement\n', str(P.complement()))
print('\nConverce\n', str(P.converce()))
print('\nDual\n', str(P.dual()))


# print(str(RELATION(size=3, type='full')))
# print(str(RELATION(size=3, type='diagonal')))
# print(str(RELATION(size=3, type='antidiagonal')))