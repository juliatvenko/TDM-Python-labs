from memory_profiler import memory_usage
import time

class RELATION_CUT:

    def __init__(self, data=None, size=None, type=None):
        self.size = size
        if data is not None:
            self.data = dict(sorted(data.items()))
            if size is None:
                self.size = max(max([k] + list(v), default=1) for k, v in self.data.items())
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
        return RELATION_CUT(intersection)

    

    def union(self, other):
        union = {}
        for key in set(self.data.keys()).union(other.data.keys()):
            union[key] = self.data.get(key, set()).union(other.data.get(key, set()))
        return RELATION_CUT(union)

    

    def difference(self, other):
        difference = {}
        for key in self.data.keys():
            difference[key] = self.data.get(key, set()).difference(other.data.get(key, set()))
        return RELATION_CUT(difference)



    def sym_diff(self, other):
        symmetric_difference = {}
        for key in self.data.keys():
            symmetric_difference[key] = self.data.get(key, set()).symmetric_difference(other.data.get(key, set()))
        return RELATION_CUT(symmetric_difference)

    
    def complement(self):
        complement = {}
        full = RELATION_CUT(size=self.size, type ='full')
        for key, value in full.data.items():
            complement[key] = value - self.data.get(key, set())
        return RELATION_CUT(complement)

    
    def converce(self):
        converse = {}
        for i, related in self.data.items():
            for j in related:
                converse.setdefault(j, set()).add(i)
        return RELATION_CUT(converse)


    def dual(self):
        return RELATION_CUT(RELATION_CUT(self.complement().data).data).converce()


    def composition(self, other):
        composition = {}
        for p_key, p_values in self.data.items():
            for q_key, q_values in other.data.items():
                if p_key in q_values:
                    composition.setdefault(q_key, set()).update(p_values)
        return RELATION_CUT(composition)

    def is_subset(self, other):
        for key, values in self.data.items():
            if key not in other.data or not values.issubset(other.data[key]):
                return False
        return True
    
    def is_reflexive(self):
        return RELATION_CUT(size=self.size, type='diagonal').is_subset(self)
    
    def is_antireflexive(self):
        return self.is_subset(RELATION_CUT(size=self.size, type='antidiagonal'))
    
    def is_symmetric(self):
        return self.is_subset(self.converce())

    def is_asymmetric(self):
        return self.intersection(self.converce()).data == set()
    
    def is_antysymmetric(self):
        return self.intersection(self.converce()).is_subset(\
            RELATION_CUT(size=self.size, type='diagonal'))

    def is_transitive(self):
        return self.composition(self).is_subset(self)

    def is_connected(self):
        return self.union(self.converce()).difference(RELATION_CUT(size=self.size, type='diagonal')).data \
              == RELATION_CUT(size=self.size, type='antidiagonal').data
    

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
        return RELATION_CUT(self.relations.intersection(self.converce().data))
    
 
    def asymmetric_part(self):
        return RELATION_CUT(self.relations.difference(self.symmetric_part().data))
    

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
        pass

    def transitive_closure(self):
        pass

    def reachability(self, start):
        pass

    def is_mutually_reachable(self, a, b):
        pass

    def factorized(self):
        pass

# P = RELATION_MATR(size=4, data=[[1, 0, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [0, 0, 1, 1]])
# Q = RELATION_MATR(size=4, data=[[0, 0, 1, 1], [1, 1, 1, 0], [0, 1, 1, 1], [0, 1, 1, 0]]) 
# P = RELATION_CUT({1: {1, 3}, 2: {2}, 3: {1, 2, 3, 4}, 4: {2, 3, 4}}, size=4)
# Q = RELATION_CUT({1: {2}, 2: {2, 3, 4}, 3: {1, 2, 3, 4}, 4: {1, 3}}, size=4)

# P = RELATION_CUT({1: {2, 3}, 2: set(), 3: {2, 4}, 4: {1, 2}, 5: {1, 3}}, size=5)
# Q = RELATION_CUT({1: set(), 2: {3, 4}, 3: set(), 4: {5}, 5: {2, 3}}, size=5)
# R = RELATION_CUT({1: {4}, 2: {3, 5}, 3: {4, 5}, 4: {1}, 5: {2, 4}}, size=5)
# print('Intersection\n', str(P.intersection(Q)))
# print('\nUnion\n', str(P.union(Q)))
# print('\nDifference\n', str(P.difference(Q)))
# print('\nSymmetric difference\n', str(P.sym_diff(Q)))
# print('\nComposition\n', str(P.composition(Q)))
#print('\nComplement\n', str(P.complement()))
# print('\nConverce\n', str(P.converce()))
# print('\nDual\n', str(P.dual()))

# print("P = ", str(P))
# print("Q = ", str(Q))
# print("R = ", str(R))

# mem_usage_before = memory_usage(-1, interval=0.1, timeout=1)[0]
# start_time = time.time()  

# K = P.composition(Q).difference(R.dual())

# end_time = time.time() 
# mem_usage_after = memory_usage(-1, interval=0.1, timeout=1)[0]

# K = P.composition(Q).difference(R.dual())
# print('\nK = (P∘Q)\R^d =', str(K))

# print(f"Memory used: {mem_usage_after - mem_usage_before} MiB")
# print(f"Time taken: {end_time - start_time} seconds")

#print(str(RELATION_CUT(size=4, type='full')))
# print(str(RELATION(size=3, type='diagonal')))
# print(str(RELATION(size=3, type='antidiagonal')))