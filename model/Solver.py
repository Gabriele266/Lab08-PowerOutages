from database.DAO import DAO
from model.PartialSolution import PartialSolution
from model.powerOutages import Event

class Solver:
    def __init__(self, X: int, Y: int, nerc_id: int):
        self.__x = X
        self.__y = Y
        self.__nerc_id = nerc_id
        self.blackout_list: list[Event] = DAO.getAllEventsByNercId(nerc_id)
        self.__optimal_solution: PartialSolution | None = None
        self.__admissible_cache: list[PartialSolution] = []

    def solve(self, k = 1, previous_partial: PartialSolution | None = None):
        tot = len(self.blackout_list)

        if k > tot:
            return          # Ho finito le possibili soluzioni da esplorare

        available_events = []
        if k == 1 and previous_partial is None:
            available_events = self.blackout_list

        if k > 1 and previous_partial is not None:
            available_events = set(self.blackout_list) - set(previous_partial.blackout_events)    # Lista di tutti gli id che posso utilizzare per esplorare nuove combinazioni senza fare ripetizioni

        if len(available_events) == 0:
            return

        for evt in available_events:
            prev_evts = []
            if previous_partial is not None:
                prev_evts += previous_partial.blackout_events

            sol = PartialSolution(
                prev_evts + [evt]
            )
            print(sol)
            self.check_solution(sol)
            # espando aggiungendo un livello alla soluzione che stavo già guardando
            self.solve(k + 1, sol)

    def check_solution(self, sol: PartialSolution):
        # Controllo questa soluzione
        if self.check_admissible(sol):
            sol.is_ammissible = True
            self.__admissible_cache.append(sol)

            if self.__optimal_solution is None:
                self.__optimal_solution = sol
            elif self.__optimal_solution is not None and self.check_optimal(sol):
                self.__optimal_solution = sol

    def check_admissible(self, sol: PartialSolution) -> bool:
        return True     # TODO

    def check_optimal(self, sol: PartialSolution) -> bool:
        return True     # TODO

    def get_event_by_id(self, id: int) -> Event:
        for evt in self.blackout_list:
            if evt.id == id:
                return evt

        raise ValueError(str(id))

