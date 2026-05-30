import time

import flet as ft

from exceptions.SolverException import SolverException
from model.Solver import Solver
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
        if self._model.max_years == 0 or self._model.max_hours == 0 or self._model.nerc_id == 0:
            self._view.create_alert("Non sono stati inseriti tutti i parametri")
            return

        solver = Solver(
            max_hours=self._model.max_hours,
            max_years=self._model.max_years,
            nerc_id=self._model.nerc_id
        )

        t1 = time.time()
        solver.solve()
        t2 = time.time()

        out = ""
        try:
            optimal = solver.optimal_solution
            r = t2 - t1
            print(f"Solved problem in {r}s")
            print(f"Optimal solution found: {optimal}")
            out = f"""
            Selected nerc has {solver.total_blackout_count} events total.
            Solution found in {r} seconds
            Solution content: [
                {optimal.__str__()}
            ]
            """
        except SolverException as e:
            print(e)
            out = e.__str__()

        self._view._txtOut.controls = [(ft.Text(
            out
        ))]
        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(text=n.value, key=n.id))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def handle_max_years_change(self, event):
        self._model.max_years = int(event.data)

    def handle_max_hours_change(self, event):
        self._model.max_hours = int(event.data)

    def handle_nerc_select(self, event):
        self._model.nerc_id = int(event.data)