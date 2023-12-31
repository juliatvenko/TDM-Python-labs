from abc import ABC, abstractmethod

class RELATION(ABC):
    def __init__(self, relations=None, size=None, type=None): 
        self.size = size
        if relations is not None:
            self.relations = set(sorted(relations))
            if size is None:
                try:
                    self.size = max(max(pair) for pair in self.relations) + 1
                except ValueError:  
                    self.size = 0
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
    

    def intersection(self, other):
        return RELATION(self.relations.intersection(other.relations))


    def union(self, other):
        return RELATION(self.relations.union(other.relations))
    

    def difference(self, other):
        return RELATION(self.relations.difference(other.relations))
    

    def sym_diff(self, other):
        return RELATION(self.relations.symmetric_difference(other.relations))


    def complement(self):
        return RELATION(RELATION(size=self.size, type='full').relations - self.relations)
    

    def converce(self):
        return RELATION({(y, x) for (x, y) in self.relations})
    

    def composition(self, other):
        return RELATION({(x, y) for x, z1 in self.relations for z2, y in other.relations if z1 == z2})
    

    def dual(self):
        return RELATION(RELATION(self.complement().relations).relations).converce()
    

    def is_subset(self, other):
        return self.relations.issubset(other.relations)
    

    def is_reflexive(self):
        return RELATION(size=self.size, type='diagonal').is_subset(self)
    

    def is_antireflexive(self):
        return self.is_subset(RELATION(size=self.size, type='antidiagonal'))
    

    def is_symmetric(self):
        return self.is_subset(self.converce())


    def is_asymmetric(self):
        return self.intersection(self.converce()).relations == set()
    

    def is_antysymmetric(self):
        return self.intersection(self.converce()).is_subset(RELATION(size=self.size, type='diagonal'))
    

    def is_transitive(self):
        return self.composition(self).is_subset(self) 
    

    def is_acyclic(self):
        graph = {node: [] for pair in self.relations for node in pair}
        for a, b in self.relations:
            graph[a].append(b)
        
        def has_cycle(node, path):
            if node in path:
                return True
            path.add(node)
            for neighbor in graph[node]:
                if has_cycle(neighbor, path):
                    return True
            path.remove(node)
            return False
        return not any(has_cycle(node, set()) for node in graph)


    def is_connected(self):
        return self.union(self.converce()).difference(RELATION(size=self.size, type='diagonal')).relations \
              == RELATION(size=self.size, type='antidiagonal').relations
    

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
        return RELATION(self.relations.intersection(self.converce().relations))
    

    def asymmetric_part(self):
        return RELATION(self.relations.difference(self.symmetric_part().relations))
    
 
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
    
  
    def transitive_closure(self):
        while True:
            new_relations = set((x,w) for x,y in self.relations for q,w in self.relations if q == y)
            
            if not new_relations.issubset(self.relations): 
                self.relations = self.relations.union(new_relations)
            else:
                break  
            
        return RELATION(self.relations)
    
 
    def reachability(self, start):
        reachable = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current not in reachable:
                reachable.add(current)
                stack.extend(b for a, b in self.relations if a == current)
        return reachable
    

    def is_mutually_reachable(self, a, b):
        return a in self.reachability(b) and b in self.reachability(a)

    # @abstractmethod    
    # def factorized(self):
    #     elements = set(x for pair in self.relation for x in pair)
    #     classes = set()
    #     for a in elements:
    #         if any(a in eq_class for eq_class in classes):
    #             continue  
    #         new_class = {a}
    #         for b in elements - new_class:
    #             if self.is_mutually_reachable(a, b):
    #                 new_class.add(b)
    #         classes.add(frozenset(new_class))
    #     return classes

#Q = RELATION(relations={(0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2)})
# Reflexivity
# P = RELATION(relations={(0, 0), (0, 2), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3), (3, 2), (3, 3)})
# Antireflexivity
# P = RELATION(relations={(0, 2), (1, 2), (1, 3), (2, 0), (2, 3), (3, 2)})
# Symmetric
# P = RELATION(relations={(0, 0), (0, 2), (2, 0), (2, 2), (2, 3), (3, 2), (3, 3)})
# Asymmetric
# P = RELATION(relations={(1, 2), (1, 3), (2, 0), (3, 2)})
# Transitive
# P = RELATION(relations={(1,2), (2,3), (1,3)})
# Acyclic
# P = RELATION(relations={(1,2), (2,3), (3,4), (4,1)})
# Connected
#P = RELATION(relations={(0,1),(0,2),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,0),(3,1),(3,2)})
# Tolerant 
# P = RELATION(relations={(0, 0), (0, 2), (1, 1), (2, 0), (2, 2), (2, 3), (3, 2), (3, 3)})
# Equivalent
# P = RELATION(relations={(0, 0), (0, 2), (0, 3), (1, 1), (2, 0), (2, 2), (2, 3), (3, 0), (3, 2), (3, 3)})
# Transitive closure
#P = RELATION(relations={(1,2), (2,3)})

# print('Intersection\n', P.intersection(Q))
# print('\nUnion\n', P.union(Q))
# print('\nDifference\n', P.difference(Q))
# print('\nSymmetric difference\n', P.sym_diff(Q))
# print('\nComposition\n', P.composition(Q))
# print('\nComplement\n', str(P.complement()))
# print('\nConverce\n', str(P.converce()))
# print('\nDual\n', str(P.dual()))

# print('\nIs P reflexive\n', P.is_reflexive())
# print('\nIs P antireflexive\n', P.is_antireflexive())
# print('\nIs P symmetric\n', P.is_symmetric())
# print('\nIs P asymmetric\n', P.is_asymmetric())
# print('\nIs P transitive\n', P.is_transitive())
# print('\nIs P acyclic\n', P.is_acyclic())
# print('\nIs P connected\n', P.is_connected())
# print('\nIs P tolerant\n', P.is_tolerant())
# print('\nIs P equivalent\n', P.is_equivalent())

# print('\nP symmetric part\n', P.symmetric_part())
# print('\nP asymmetric part\n', P.asymmetric_part())
# print('\nP transitive closure\n', P.transitive_closure())
# if not P.is_transitive():
#     P_transitive_closure = P.transitive_closure()
#     print('\nP transitive closure\n', P_transitive_closure)
#     print('\nIs P transitive closure transitive \n', P_transitive_closure.is_transitive())
#print('\nP reachable nodes\n', P.reachability(2))

# print(str(RELATION(size=3, type='full')))
# print(str(RELATION(size=3, type='diagonal')))
# print(str(RELATION(size=3, type='antidiagonal')))

# print('P properties\n' + "\n".join(f"{prop}: {val}" for prop, val in P.check_properties().items()))
# print('P type\n' + "\n".join(f"{prop}: {val}" for prop, val in P.check_type().items()))