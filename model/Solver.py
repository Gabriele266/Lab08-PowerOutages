from database.DAO import DAO
from model.PartialSolution import PartialSolution
from model.powerOutages import Event

class Solver:
    """
    Classe per risolvere il problema PL, con caching
    """
    def __init__(self, X: int, Y: int, nerc_id: int):
        self.__x = X
        self.__y = Y
        self.__nerc_id = nerc_id
        self.blackout_list: list[Event] = DAO.getAllEventsByNercId(nerc_id)
        self.__optimal_solution: PartialSolution | None = None
        self.__solutions_cache: list[PartialSolution] = []              # Cache con tutte le soluzioni già esplorate
        self.__not_admissible_cache: list[set[int]]= []                # Lista con tutti i vettori di id che danno luogo a soluzioni non ammissibili

    def solve(self, k = 1, previous_partial: PartialSolution | None = None):
        """
        Effettua la risoluzione del problema di programmazione lineare
        partendo da k = 1 fino a quando ci sono soluzioni possibili.
        Esplora tutte le combinazioni di possibili eventi
        """
        tot = len(self.blackout_list)

        if k > tot or (previous_partial is not None and previous_partial.is_ammissible == False):
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
            if self.__it_cant_be_admissible(sol.blackout_ids):
                self.__not_admissible_cache.append(sol.blackout_ids)        # La aggiungo alla cache dei non ammissibili per rendere il controllo la prossima volta più semplice
                continue                # Procedo con la prossima soluzione, questa so già che non è ammissibile
            elif not self.__check_in_cache(sol):            # Non so se sia ammissibile o meno ma non è in nessuna delle due cache
                sol.calc_aggregates()  # Effettuo il calcolo delle statistiche aggregate
                if self.__check_admissible(sol):            # Controllo l'ammissibilità della soluzione
                    sol.is_ammissible = True
                    # Controllo ottimalità
                    if self.__optimal_solution is None:
                        self.__optimal_solution = sol
                    elif self.__optimal_solution is not None and self.__check_optimal(sol):
                        self.__optimal_solution = sol

                    self.__append_to_cache(sol)     # Aggiungo alla cache
                    print(sol)
                    # espando aggiungendo un livello alla soluzione che stavo già guardando
                    self.solve(k + 1, sol)
                else:       # Soluzione non ammissibile, aggiungo i suoi id alla cache delle soluzioni non ammissibili per evitare di ri-fare tutti i calcoli un'altra volta
                    sol.is_ammissible = False
                    self.__not_admissible_cache.append(sol.blackout_ids)        # Li mantengo ordinati così il controllo è solo un'uguaglianza
                    # Nota: aggiungere qualcosa ad una soluzione che non è ammissibile non porta sicuramente ad avere una soluzione ammissibile, quindi è inutile espandere ulteriormente la ricerca su quel ramo

    def __it_cant_be_admissible(self, sol_ids: set[int]):
        """
        Controlla se so già a priori che questa soluzione non può essere ammissibile solo guardando gli id
        Restituisce True se so già che questa soluzione non può essere ammissibile
        """
        # L'insieme di ID è già nella cache dei non ammissibili (indifferentemente dall'ordine)
        # L'insieme di ID è un superset di uno degli insiemi già presenti nella cache dei non ammissibili --> Aggiungendo qualcosa non posso ottenere un valore ammissibile
        for ids in self.__not_admissible_cache:
            if ids.issubset(sol_ids):
                return True

        return False

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
        """Restituisce la soluzione ottima trovata dall'algoritmo se esiste"""
        if self.__optimal_solution is not None:
            return self.__optimal_solution
        raise Exception("No optimal solution found (check if you have called solve() )")

    def __check_admissible(self, sol: PartialSolution) -> bool:
        """
        Controlla l'ammissibilità della soluzione
        """
        return sol.total_covered_hours <= self.__x and sol.total_covered_years <= self.__y

    def __check_optimal(self, sol: PartialSolution) -> bool:
        """
        Controlla l'ottimalità della soluzione rispetto alla soluzione attualmente ottima
        """
        return sol.total_customers > self.__optimal_solution.total_customers