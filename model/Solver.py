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
        self.__solutions_cache: list[PartialSolution] = []              # Cache con tutte le soluzioni già esplorate

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

            sol = PartialSolution(          # Creo la nuova soluzione da esplorare (non contiene ancora le statistiche aggregate)
                prev_evts + [evt]
            )
            if not self.__check_in_cache(sol):
                sol.calc_aggregates()            # Effettuo il calcolo delle statistiche aggregate
                self.check_solution(sol)        # Controllo che sia ammissibile e se è ottima
                print(f"Unique solution found: {sol}")
                self.__append_to_cache(sol)     # Aggiungo alla cache

            # espando aggiungendo un livello alla soluzione che stavo già guardando
            self.solve(k + 1, sol)

    def check_solution(self, sol: PartialSolution):
        # Controllo questa soluzione
        if self.check_admissible(sol):
            sol.is_ammissible = True
            if self.__optimal_solution is None:
                self.__optimal_solution = sol
            elif self.__optimal_solution is not None and self.check_optimal(sol):
                self.__optimal_solution = sol
        else:
            sol.is_ammissible = False

    def __append_to_cache(self, solution: PartialSolution):
        """Aggiunge la soluzione in cache solo se non è ancora stata esplorata. """
        self.__solutions_cache.append(solution)

    def __check_in_cache(self, solution: PartialSolution) -> bool:
        for s in self.__solutions_cache:
            if s.__eq__(solution):
                return True

        return False

    @property
    def optimal_solution(self):
        if self.__optimal_solution is not None:
            return self.__optimal_solution
        raise Exception("No optimal solution found (check if you have called solve() )")

    def check_admissible(self, sol: PartialSolution) -> bool:
        """
        Controlla l'ammissibilità della soluzione
        """
        return sol.total_covered_hours <= self.__x and sol.total_covered_years <= self.__y

    def check_optimal(self, sol: PartialSolution) -> bool:
        """
        Controlla l'ottimalità della soluzione rispetto alla soluzione attualmente ottima
        """
        return sol.total_customers > self.__optimal_solution.total_customers

    def get_event_by_id(self, id: int) -> Event:
        for evt in self.blackout_list:
            if evt.id == id:
                return evt

        raise ValueError(str(id))

