Problem:
We want to make pairings for a tournament round for N players, satisfying the conditions
- Two players that have already faced each other before cannot face each other again.
- Maximum of one player can be omitted (have a "Bye"). It can't be a player that has already had a bye.
- Players of as much of a similar score as possible should be matched with each other.


Solution:
We can model this with a graph with N vertices, representing the players, where there is an edge between player i and j if they haven't faced each other before.
If each edge has a weight of abs(score(i)-score(j)) then getting the optimal solution would amount to a maximum cardinality minimum weight matching of the graph, which provides us with a pairing that 
minimizes the sum of the score differences between competing players.

Implementation notes:
- The library used is rustworkx, which works much faster than networkx.
- We can get a minimum weight matching by calling a maximum weight watching with negative edge weights.
- A Bye is modeled by a fictional N+1-th player that is connected to all players that can take a Bye with a 0 edge weight.
- The algorithm used works in O(N^3) time. This could be improved by implementing [newer algorithms](https://web.eecs.umich.edu/~pettie/papers/ApproxMWM-JACM.pdf).
