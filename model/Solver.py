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

        if k == 1 and previous_partial == None:
            level_one = []                  # Creo la lista delle soluzioni di primo livello (con 1 elemento dentro)

            for evt in self.blackout_list:
                sol = PartialSolution(
                    blackout_ids=[evt.id],
                    total_covered_years=1,
                    total_customers=evt.customers_affected,
                    total_covered_hours=evt.duration,
                    is_optimal=None,
                    is_ammissible=None
                )
                level_one.append(sol)

                # Controllo questa soluzione
                if self.check_admissible(sol):
                    sol.is_ammissible = True
                    self.__admissible_cache.append(sol)

                    if self.__optimal_solution is None:
                        self.__optimal_solution = sol
                    elif self.__optimal_solution is not None and self.check_optimal(sol):
                        self.__optimal_solution = sol

                # espando aggiungendo un livello alla soluzione che stavo già guardando
                self.solve(k + 1, sol)


    def check_admissible(self, sol: PartialSolution) -> bool:
        return True     # TODO

    def check_optimal(self, sol: PartialSolution) -> bool:
        return True     # TODO

