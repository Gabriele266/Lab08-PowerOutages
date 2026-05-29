from model.powerOutages import Event

class PartialSolution:
    """
    Rappresenta una soluzione parziale del problema PL
    Quando viene istanziata, le statistiche aggregate sulla soluzione NON VENGONO CALCOLATE SUBITO,
    per ragioni di ottimizzazione.
    Il solver ne ordina il calcolo dopo aver verificato di non aver ancora esplorato questa soluzione.
    """
    def __init__(self, blackout_events: list[Event]):
        if len(blackout_events) == 0:
            raise ValueError("An empty solution is not ammissible")

        self.__blackout_ids: set[int] = set(sorted(
            map(lambda e: e.id, blackout_events)))  # Set ordinato degli id scelti in questa soluzione
        self.__blackout_events: list[Event] = blackout_events  # Lista di descrittori
        self.__total_covered_years: int = 0  # Differenza tra l'anno più recente e l'anno più vecchio
        self.__total_covered_hours: int = 0  # Numero totale di ore coperte
        self.__total_customers: int = 0  # Valore della funzione obiettivo
        self.is_ammissible: bool | None = None  # Indica se questa soluzione è ammissibile per il problema (None quando non è ancora stato verificato)
        self.__is_optimal: bool | None = None  # Indica se è la soluzione ottima

    def calc_target_function(self):
        """Calcola la funzione obiettivo"""
        self.__total_customers = sum(map(lambda e: e.customers_affected, self.blackout_events), 0)

    def calc_aggregates(self):
        """Calcola tutte le statistiche aggregate sulla soluzione"""
        unique_years = sorted(set(map(lambda e: e.year, self.blackout_events)))

        self.__blackout_events = self.blackout_events
        self.__total_covered_years  = abs(unique_years[-1] - unique_years[0])
        self.__total_covered_hours = sum(map(lambda e: e.duration, self.blackout_events), 0)
        self.calc_target_function()
        self.is_ammissible = None
        self.__is_optimal = None

    @property
    def blackout_ids(self):
        return self.__blackout_ids

    @property
    def blackout_events(self):
        return self.__blackout_events

    @property
    def total_covered_years(self):
        return self.__total_covered_years

    @property
    def total_covered_hours(self):
        return self.__total_covered_hours

    @property
    def total_customers(self):
        return self.__total_customers

    @property
    def is_optimal(self):
        return self.__is_optimal

    @is_optimal.setter
    def is_optimal(self, value):
        if not self.is_ammissible:
            raise ValueError("Tried to set an optimal value on an inammissible solution")
        self.__is_optimal = value

    def __eq__(self, other):
        """
        Due soluzioni sono identiche se contengono la stessa lista di ID, anche non nello stesso ordine
        """
        return sorted(self.blackout_ids) == sorted(other.blackout_ids)

    def __str__(self):
        return f"""
        Partial solution with {len(self.blackout_events)} events.
        {[ f"{e.id}," for e in self.blackout_events]}
        Total customers: {self.__total_customers} = z
        Admissible: {self.is_ammissible}
        Duration: {self.__total_covered_hours}
        Years: {self.__total_covered_years}\n
        """