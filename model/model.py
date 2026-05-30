from database.DAO import DAO
from model.nerc import Nerc


class Model:
    def __init__(self):
        self.max_years = 0
        self.max_hours = 0
        self.nerc_id = 0

    @property
    def listNerc(self) -> list[Nerc]:
        return DAO.getAllNerc()