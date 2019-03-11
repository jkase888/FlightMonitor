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

tripA = tripSearch()
tripA.origin="yyz"
tripA.destination="mco"
tripA.departureDate="2019-04-20"
tripA.returnDate="2019-04-29"
tripA.adults="1"
tripA.children="0"
tripA.travelClass="ECONOMY"
tripA.nonStop="true"
tripA.currency="CAD"
tripA.max="50"
tripA.includeAirlines="AC"

tripA.targetDepartureFlightNumber="1672"
tripA.targetArrivalFlightNumber="1677"

try:

    #connect to database
    db = DatabaseGateway()
    db.connect()

    response = amadeus.shopping.flight_offers.get(origin=tripA.origin, destination=tripA.destination,
                departureDate=tripA.departureDate, returnDate=tripA.returnDate, adults=tripA.adults,
                children=tripA.children, travelClass=tripA.travelClass, nonStop=tripA.nonStop, currency=tripA.currency,
                max=tripA.max, includeAirlines=tripA.includeAirlines)
    jsonObject = json.loads(response.body)


    for data in jsonObject['data']:
        for offerItems in data['offerItems']:
            firstSegementIsFound = False
            secondSegementIsFound = False
            for serviceItems in offerItems['services']:
                if (serviceItems['segments'][0]['flightSegment']['number'] == tripA.targetDepartureFlightNumber) and (firstSegementIsFound == False):
                    firstSegementIsFound = True
                if (serviceItems['segments'][0]['flightSegment']['number'] == tripA.targetArrivalFlightNumber) and (firstSegementIsFound == True):
                    secondSegementIsFound = True
            if (firstSegementIsFound) and (secondSegementIsFound):
                datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
                offerItems['datetimestamp'] = datetimestampStr
                strOfferItems = json.dumps(offerItems)

                db.insertAirlinePrice(from_code=tripA.targetDepartureFlightNumber, return_code=tripA.targetArrivalFlightNumber, date_depature=tripA.departureDate, date_return=tripA.returnDate, total_price=tripA.offerItems['price']['total'], logged_at_datetime=datetimestampStr)

                '''
                # output raw log of json
                #f = open(path + "raw_log.txt", "a")
                f = open("raw_log.txt", "a")
                f.write(strOfferItems)
                f.write("\n\n")
                f.close()

                # output short log
                #f = open(path + "short_log.txt", "a")
                f = open("short_log.txt", "a")
                f.write(('"' + datetimestampStr + '",' + targetDepartureFlightNumber + ',' + targetArrivalFlightNumber + ',' + offerItems['price']['total'] + '\n'))
                f.close()
                '''
    datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
    print(datetimestampStr)
    db.close()

except ResponseError as error:
    print(error)
