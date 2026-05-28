
from dataclasses import dataclass

@dataclass
class PartialSolution:
    blackout_ids: list[int]         # Lista degli id scelti in questa soluzione
    total_covered_years: int        # Numero di anni a partire da oggi che sono coperti
    total_covered_hours: int        # Numero totale di ore coperte
    total_customers: int            # Valore della funzione obiettivo
    is_ammissible: bool | None      # Indica se questa soluzione è ammissibile per il problema (None quando non è ancora stato verificato)
    is_optimal: bool | None         # Indica se è la soluzione ottima

    def __eq__(self, other):
        """
        Due soluzioni sono identiche se contengono la stessa lista di ID, anche non nello stesso ordine
        """
        return self.blackout_ids.sort() == other.blackout_ids.sort()