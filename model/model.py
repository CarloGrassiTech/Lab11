import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.MultiGraph()
        self._nodes = []
        self._edges = []
        self._anno = None
        self._colore = None
        self._idMap = {}


    def buildGraph(self):
        self._nodes = DAO.getAllNodes(self._colore)
        for n in self._nodes:
            self._idMap[n.Product_number] = n
        self._graph.add_nodes_from(self._nodes)
        self._edges = DAO.getAllEdges(self._anno, self._colore)
        for i in self._edges:
            self._graph.add_edge(self._idMap[i[0]],self._idMap[i[1]], weight = int(i[2]))

    def agetAllColor(self):
        return DAO.getAllColor()