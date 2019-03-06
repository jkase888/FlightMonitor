from amadeus import Client, ResponseError
from database import DatabaseGateway
import json
import datetime
import pytz
import os

#path = "/Users/asethia/Documents/App/FlightMonitor/"

amadeus = Client(
    #client_id=os.environ['client_id'],
    #client_secret=os.environ['client_secret'],
    client_id=os.environ['client_id_test'],
    client_secret=os.environ['client_secret_test'],
    #hostname='production'
)

origin="yyz"
destination="mco"
departureDate="2019-04-20"
returnDate="2019-04-29"
adults="1"
children="0"
travelClass="ECONOMY"
nonStop="true"
currency="CAD"
max="50"
includeAirlines="AC"

targetDepartureFlightNumber="1672"
targetArrivalFlightNumber="1677"

try:

    #connect to database
    db = DatabaseGateway()
    db.connect()

    response = amadeus.shopping.flight_offers.get(origin=origin, destination=destination,
                departureDate=departureDate, returnDate=returnDate, adults=adults,
                children=children, travelClass=travelClass, nonStop=nonStop, currency=currency,
                max=max, includeAirlines=includeAirlines)
    jsonObject = json.loads(response.body)


    for data in jsonObject['data']:
        for offerItems in data['offerItems']:
            firstSegementIsFound = False
            secondSegementIsFound = False
            for serviceItems in offerItems['services']:
                if (serviceItems['segments'][0]['flightSegment']['number'] == targetDepartureFlightNumber) and (firstSegementIsFound == False):
                    firstSegementIsFound = True
                if (serviceItems['segments'][0]['flightSegment']['number'] == targetArrivalFlightNumber) and (firstSegementIsFound == True):
                    secondSegementIsFound = True
            if (firstSegementIsFound) and (secondSegementIsFound):
                datetimestampStr = datetime.datetime.now(pytz.timezone('US/Eastern')).__str__()
                offerItems['datetimestamp'] = datetimestampStr
                strOfferItems = json.dumps(offerItems)

                db.insertAirlinePrice(from_code=targetDepartureFlightNumber, return_code=targetArrivalFlightNumber, date_depature=departureDate, date_return=returnDate, total_price=offerItems['price']['total'], logged_at_datetime=datetimestampStr)

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
