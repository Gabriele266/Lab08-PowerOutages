import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        nerc = self._idMap[self._view._ddNerc.value]
        maxY = self._view._txtYears.value
        maxH = self._view._txtHours.value
        self._model.worstCase(nerc, int(maxY), int(maxH))

        self._view._txtOut.controls.clear()
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {self._model.countCustomers(self._model._solBest)}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {self._model.sumDurata(self._model._solBest)/60/60}"))

        for v in self._model._solBest:
            self._view._txtOut.controls.append(ft.Text(f"{v}"))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            # self._view._ddNerc.options.append(ft.dropdown.Option(n))
            self._view._ddNerc.options.append(ft.dropdown.Option(text=n.value,
                                                                     data=n,
                                                                     on_click=self.readDD))
            self._view.update_page()

    def readDD(self,e):
        print(e.control.data)
        pass
    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
