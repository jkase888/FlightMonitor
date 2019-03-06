from amadeus import Client, ResponseError
import json
import datetime

#path = "/Users/asethia/Documents/App/FlightMonitor/"


amadeus = Client(
    client_id=os.environ['client_id'],
    client_secret=os.environ['client_secret'],
    hostname='production'
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
                datetimestampStr = datetime.datetime.now().__str__()
                offerItems['datetimestamp'] = datetimestampStr
                strOfferItems = json.dumps(offerItems)
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
    datetimestampStr = datetime.datetime.now().__str__()
    print(datetimestampStr)

except ResponseError as error:
    print(error)
