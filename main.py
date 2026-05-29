import flet as ft

from model.Solver import Solver
from model.model import Model
from UI.view import View
from UI.controller import Controller


def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()
    s = Solver(20, 30, 2)
    s.solve()
    optimal = s.optimal_solution
    print("Soluzione ottima: ")
    print(optimal)

ft.app(target=main)
