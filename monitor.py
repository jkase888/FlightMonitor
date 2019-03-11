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

tripB = TripSearch(origin="yyz",destination="mco",departureDate="2019-05-17",returnDate="2019-05-20",adults="1",children="0",travelClass="ECONOMY",nonStop="true",currency="CAD",max="50",includeAirlines="AC",targetDepartureFlightNumber="1670",targetArrivalFlightNumber="1677")

tripC = TripSearch(origin="yyz",destination="mco",departureDate="2019-06-29",returnDate="2019-07-07",adults="1",children="0",travelClass="ECONOMY",nonStop="true",currency="CAD",max="50",includeAirlines="WS",targetDepartureFlightNumber="1226",targetArrivalFlightNumber="1241")

tripD = TripSearch(origin="yyz",destination="yvr",departureDate="2019-08-17",returnDate="2019-08-25",adults="1",children="0",travelClass="ECONOMY",nonStop="true",currency="CAD",max="50",includeAirlines="AC",targetDepartureFlightNumber="101",targetArrivalFlightNumber="182")

trigger_hours = [1, 5, 9, 14, 17, 21]
current_hour = datetime.datetime.now(pytz.timezone('US/Eastern')).hour
if (current_hour not in trigger_hours):
    sys.exit()

try:

    #connect to database
    db = DatabaseGateway()
    db.connect()

    trip = tripA
    # << trip start
    response = amadeus.shopping.flight_offers.get(origin=trip.origin, destination=trip.destination,
                departureDate=trip.departureDate, returnDate=trip.returnDate, adults=trip.adults,
                children=trip.children, travelClass=trip.travelClass, nonStop=trip.nonStop, currency=trip.currency,
                max=trip.max, includeAirlines=trip.includeAirlines)
    jsonObject = json.loads(response.body)

    if (trip.search(jsonDataObject=jsonObject['data'])):
        db.insertAirlinePrice(from_code=trip.targetDepartureFlightNumber, return_code=trip.targetArrivalFlightNumber, date_depature=trip.departureDate, date_return=trip.returnDate, total_price=trip.totalPrice, logged_at_datetime=trip.loggedAtDatetime)

    datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
    print("trip A: " + datetimestampStr)
    # trip end >>

    trip = tripB
    # << trip start
    response = amadeus.shopping.flight_offers.get(origin=trip.origin, destination=trip.destination,
                departureDate=trip.departureDate, returnDate=trip.returnDate, adults=trip.adults,
                children=trip.children, travelClass=trip.travelClass, nonStop=trip.nonStop, currency=trip.currency,
                max=trip.max, includeAirlines=trip.includeAirlines)
    jsonObject = json.loads(response.body)

    if (trip.search(jsonDataObject=jsonObject['data'])):
        db.insertAirlinePrice(from_code=trip.targetDepartureFlightNumber, return_code=trip.targetArrivalFlightNumber, date_depature=trip.departureDate, date_return=trip.returnDate, total_price=trip.totalPrice, logged_at_datetime=trip.loggedAtDatetime)

    datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
    print("trip B: " + datetimestampStr)
    # trip end >>

    trip = tripC
    # << trip start
    response = amadeus.shopping.flight_offers.get(origin=trip.origin, destination=trip.destination,
                departureDate=trip.departureDate, returnDate=trip.returnDate, adults=trip.adults,
                children=trip.children, travelClass=trip.travelClass, nonStop=trip.nonStop, currency=trip.currency,
                max=trip.max, includeAirlines=trip.includeAirlines)
    jsonObject = json.loads(response.body)

    if (trip.search(jsonDataObject=jsonObject['data'])):
        db.insertAirlinePrice(from_code=trip.targetDepartureFlightNumber, return_code=trip.targetArrivalFlightNumber, date_depature=trip.departureDate, date_return=trip.returnDate, total_price=trip.totalPrice, logged_at_datetime=trip.loggedAtDatetime)

    datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
    print("trip C: " + datetimestampStr)
    # trip end >>

    trip = tripD
    # << trip start
    response = amadeus.shopping.flight_offers.get(origin=trip.origin, destination=trip.destination,
                departureDate=trip.departureDate, returnDate=trip.returnDate, adults=trip.adults,
                children=trip.children, travelClass=trip.travelClass, nonStop=trip.nonStop, currency=trip.currency,
                max=trip.max, includeAirlines=trip.includeAirlines)
    jsonObject = json.loads(response.body)

    if (trip.search(jsonDataObject=jsonObject['data'])):
        db.insertAirlinePrice(from_code=trip.targetDepartureFlightNumber, return_code=trip.targetArrivalFlightNumber, date_depature=trip.departureDate, date_return=trip.returnDate, total_price=trip.totalPrice, logged_at_datetime=trip.loggedAtDatetime)

    datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
    print("trip D: " + datetimestampStr)
    # trip end >>


    db.close()

except ResponseError as error:
    print(error)
