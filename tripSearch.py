class TripSearch():
    def __init__(self, origin, destination, departureDate, returnDate, adults, children, travelClass, nonStop, currency, max, includeAirlines, targetDepartureFlightNumber, targetArrivalFlightNumber):
        self.origin=origin
        self.destination=destination
        self.departureDate=departureDate
        self.returnDate=returnDate
        self.adults=adults
        self.children=children
        self.travelClass=travelClass
        self.nonStop=nonStop
        self.currency=currency
        self.max=max
        self.includeAirlines=includeAirlines
        self.targetDepartureFlightNumber=targetDepartureFlightNumber
        self.targetArrivalFlightNumber=targetArrivalFlightNumber

    def search(self, jsonDataObject):
        for data in jsonDataObject:
            for offerItems in data['offerItems']:
                firstSegementIsFound = False
                secondSegementIsFound = False
                for serviceItems in offerItems['services']:
                    if (serviceItems['segments'][0]['flightSegment']['number'] == self.targetDepartureFlightNumber) and (firstSegementIsFound == False):
                        firstSegementIsFound = True
                    if (serviceItems['segments'][0]['flightSegment']['number'] == self.targetArrivalFlightNumber) and (firstSegementIsFound == True):
                        secondSegementIsFound = True
                if (firstSegementIsFound) and (secondSegementIsFound):
                    datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
                    self.totalPrice = offerItems['price']['total']
                    self.loggedAtDatetime = logged_at_datetime=datetimestampStr
                    return True
        return False
