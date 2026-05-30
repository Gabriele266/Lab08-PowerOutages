from database.DB_connect import DBConnect
from model.nerc import Nerc
from model.powerOutages import Event


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getAllNerc():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM Nerc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Nerc(row["id"], row["value"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEventsByNercId(nerc_id):
        """
        Restituisce tutti gli eventi che appartengono al gestore ordinati in base all'ID (per ragioni interne)
        """
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM PowerOutages WHERE nerc_id=%s ORDER BY id"""

        cursor.execute(query, (nerc_id,))

        for row in cursor:
            result.append(
                Event(row["id"], row["event_type_id"],
                      row["tag_id"], row["area_id"],
                      row["nerc_id"], row["responsible_id"],
                      row["customers_affected"], row["date_event_began"],
                      row["date_event_finished"], row["demand_loss"]))

        cursor.close()
        conn.close()
        return result