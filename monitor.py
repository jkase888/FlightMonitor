from amadeus import Client, ResponseError
from database import DatabaseGateway
from tripSearch import TripSearch
import json
import datetime
import pytz
import os

#path = "/Users/asethia/Documents/App/FlightMonitor/"

amadeus = Client(
    client_id=os.environ['client_id'],
    client_secret=os.environ['client_secret'],
    #client_id=os.environ['client_id_test'],
    #client_secret=os.environ['client_secret_test'],
    hostname='production'
)

tripA = TripSearch(origin="yyz",destination="mco",departureDate="2019-04-20",returnDate="2019-04-29",adults="1",children="0",travelClass="ECONOMY",nonStop="true",currency="CAD",max="50",includeAirlines="AC",targetDepartureFlightNumber="1672",targetArrivalFlightNumber="1677")

try:

    #connect to database
    db = DatabaseGateway()
    db.connect()

    response = amadeus.shopping.flight_offers.get(origin=tripA.origin, destination=tripA.destination,
                departureDate=tripA.departureDate, returnDate=tripA.returnDate, adults=tripA.adults,
                children=tripA.children, travelClass=tripA.travelClass, nonStop=tripA.nonStop, currency=tripA.currency,
                max=tripA.max, includeAirlines=tripA.includeAirlines)
    jsonObject = json.loads(response.body)

    if (tripA.search(jsonDataObject=jsonObject['data'])):
        db.insertAirlinePrice(from_code=tripA.targetDepartureFlightNumber, return_code=tripA.targetArrivalFlightNumber, date_depature=tripA.departureDate, date_return=tripA.returnDate, total_price=tripA.totalPrice, logged_at_datetime=tripA.loggedAtDatetime)

    datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
    print(datetimestampStr)
    db.close()

except ResponseError as error:
    print(error)
