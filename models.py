class Gyumolcsok:
    def __init__(self, id, nev):
        self.id = id
        self.nev = nev

class Partner:
    def __init__(self, az, neve, telepules):
        self.az = az
        self.neve = neve
        self.telepules = telepules

class Kisszallitasok:
    def __init__(self, datum, Partner, karton, gynev):
        self.datum = datum
        self.kontakt = Partner
        self.karton = karton
        self.gynev = gynev