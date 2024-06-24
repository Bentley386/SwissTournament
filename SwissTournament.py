import rustworkx as rx
import random


class SwissTournament:
    """
    A SwissTournament object represents a configuration of a single round of a 
    Swiss-Style tournament and allows for computation of an optimal match-up for 
    the next round.
    
    Attributes:
        numPlayers - Number of players in the tournament. This should not change between rounds.
        points - A list of size "numPlayers", i-th entry is the total amount of points the i-th player has.
        playedAgainst - A list of size "numPlayers". i-th entry is a set, which contains the indices of all players
                        i-th player has already faced. If the set contains "-1" that player has also already used a Bye.
    """
    
    def __init__(self, numPlayers : int):
        self.numPlayers = numPlayers

    def addPoints(self, points : list[int]):
        if len(points) != self.numPlayers:
            raise ValueError('Size of "points" list must be equal to the number of players.')
        self.points = points

    def addHistory(self, playedAgainst : list[set[int]]):
        if len(playedAgainst) != self.numPlayers:
            raise ValueError('Size of "playedAgainst" list must be equal to the number of players.')
        self.playedAgainst = playedAgainst
    
        
    def pairing(self):
        
        if not (hasattr(self,'points') and hasattr(self,'playedAgainst')):
            raise RuntimeError("Running the pairing function without initializing a complete configuration")
            
        #Create a graph, vertices of which are players
        G = rx.PyGraph()
        G.add_nodes_from(list(range(self.numPlayers)))      
        for i in range(self.numPlayers):
            for j in range(i+1,self.numPlayers):
                #There is an edge between players if they can face in the next round
                if j in self.playedAgainst[i]: 
                    continue
                G.add_edge(i,j,-abs(points[i]-points[j])) #Bigger differences in points are penalized more
    
        if self.numPlayers % 2 == 1: #For odd number of players, a Bye must be added
            G.add_node(self.numPlayers) #Bye is a fictional "numPlayers+1"th player.
            for i in range(self.numPlayers):
                if -1 in self.playedAgainst[i]: #Can't use Bye twice
                    continue
                G.add_edge(i,self.numPlayers,0) #No penalty for using Bye
                
                 
        pairing = rx.max_weight_matching(G, max_cardinality=True, weight_fn = lambda x : x, verify_optimum=True)
        if (self.numPlayers % 2 == 1) and (2*len(pairing) != self.numPlayers-1):
            print("Impossible to make a pairing")
        elif (self.numPlayers % 2 == 0) and (2*len(pairing) != self.numPlayers):
            print("Impossible to make a pairing")
        else:
            print("Optimal pairing found. Returning...")
            return pairing


#N=3000
#points = [random.randint(0,10) for i in range(N)]
#playedAgainst = [set() for i in range(N)]
N = 4
points = [3,3,0,0]
playedAgainst = [set() for i in range(N)]
tour = SwissTournament(N)
tour.addPoints(points)
tour.addHistory(playedAgainst)
pairs = tour.pairing()
print(pairs)
