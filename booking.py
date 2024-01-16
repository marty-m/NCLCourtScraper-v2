import datetime

class Booking:
    courtNr: int
    dateTime: datetime.datetime
    alerted: bool

    def __init__(self, courtNr, dateTime):
        self.courtNr = courtNr
        self.dateTime = dateTime
        self.alerted = False