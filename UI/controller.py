import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = [2015,2016,2017,2018]
        self._listColor = self._model.agetAllColor()
        self._ddNode = None

    def fillDD(self):
        for a in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(int(a)))
        for a in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(str(a)))


    def handle_graph(self, e):
        if self._view._ddyear.value != None and self._view._ddcolor.value != None:
            self._model._colore = str(self._view._ddcolor.value)
            self._model._anno = int(self._view._ddyear.value)
            self._model.buildGraph()
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text(f"il grafo contiene {len(self._model._nodes)} nodi e {len(self._model._edges)} archi"))
            for i in self.findMostWeightedEdges():
                self._view.txtOut.controls.append(ft.Text(f"arco tra {i[0]} a {i[1]} con peso {i[2]}"))
            self._view.update_page()
            self.fillDDProduct()

    def findMostWeightedEdges(self):
        temp = self._model._edges[0:3]
        temp.sort(key = lambda x: int(x[2]), reverse=True)
        print(temp)
        return temp
    def fillDDProduct(self):
        if self._model._graph.nodes() != None:
            for i in self._model._graph.nodes():
                self._view._ddnode.options.append(ft.dropdown.Option(key=str(i), data=i))
        self._view.update_page()

    def handle_search(self, e):
        if self._view._ddnode.value != None:
            self._ddNode = self._view._ddnode.value
        parziale = list()
        parziale.append(self._ddNode)
        nodi_rim = self._model._nodes
        nodi_rim.remove(self._ddNode)
        self.ricorsione(parziale, nodi_rim)


    def ricorsione(self, parziale, nodi_rim, costo):
        if len(nodi_rim) ==0:
            self._costo
        else:
