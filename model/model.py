from database.DAO import DAO


class Model:
    def __init__(self):
        # self._solParziale = None
        self._solBest = []
        self._clientiMaxBest = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxY, maxH):

        self.loadEvents(nerc)

        parziale = []
        # for ii, e in enumerate(self._listEvents):
        #     parziale.append(e)
        #     self.ricorsione(parziale, maxY, maxH, ii + 1)
        self.ricorsione(parziale, maxY, maxH, 0)

        print(self._solBest)
            # parziale.remove(e)

    def ricorsione(self, parziale, maxY, maxH, pos):

        # terminazione
        if self.sumDurata(parziale)/60/60 > maxH:  #self.getRangeAnni(parziale) > maxY or
            # print(f"Range{self.getRangeAnni(parziale)}")
            # print('durata: ', self.sumDurata(parziale))
            #
            # print(f"Max{maxH*60*60}")
            return

        # verifica se best
        if self.countCustomers(parziale) > self._clientiMaxBest:
            self._solBest = parziale[:]
            self._clientiMaxBest = self.countCustomers(parziale)

        # ricorsione
        i = pos
        for e in self._listEvents[pos:]: #i, e in enumerate(self._listEvents[pos:]):
            parziale.append(e)
            if self.getRangeAnni(parziale) > maxY:
                parziale.remove(e)
                return
            i+=1
            self.ricorsione(parziale, maxY, maxH, i)
            parziale.remove(e)


    def getRangeAnni(self, listOutages):
        if len(listOutages) < 2:
            return 0

        first = listOutages[0].date_event_began
        last = listOutages[-1].date_event_finished
        return int(last.year - first.year)

    def countCustomers(self, listOutages):
        if len(listOutages) == 0:
            return 0

        numCustomers = 0
        for event in listOutages:
            numCustomers += event.customers_affected
        return numCustomers

    def sumDurata(self, listOutages):
        if len(listOutages)==0:
            return 0

        sum = 0
        for event in listOutages:
            sum += self.durata(event)
        return sum
    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    def durata(self, event):
        return (event.date_event_finished - event.date_event_began).total_seconds()

    @property
    def listNerc(self):
        return self._listNerc