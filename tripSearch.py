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
