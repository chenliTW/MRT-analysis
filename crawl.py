import requests
from bs4 import BeautifulSoup
import time
import datetime
import xmltodict
import json

def get_nexttrain(station_ID):
    headers={'Content-Type': 'text/xml','SOAPAction':'http://tempuri.org/GetNextTrain2'}
    data="""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <soap:Body>
                    <GetNextTrain2 xmlns="http://tempuri.org/">
                    <stnid>{}</stnid>
                    </GetNextTrain2>
                </soap:Body>
            </soap:Envelope>""".format(station_ID)
    res=requests.post("http://ws.metro.taipei/trtcappweb/Traintime.asmx",headers=headers,data=data)
    return BeautifulSoup(res.text,'xml')

def car_stat(trip_no):
    headers={'Content-Type': 'text/xml','SOAPAction':'http://tempuri.org/GetCartDetailbyTripID'}
    data="""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <GetCartDetailbyTripID xmlns="http://tempuri.org/">
                <strCW>{}</strCW>
                </GetCartDetailbyTripID>
            </soap:Body>
            </soap:Envelope>""".format(trip_no)
    res=requests.post("http://ws.metro.taipei/trtcappweb/CartWeight.asmx",headers=headers,data=data)
    return BeautifulSoup(res.text,'xml')

out={}
trip_no=""

while 1:
    print(get_nexttrain("077").find("Detail"))
    if get_nexttrain("077").find("Detail")['tripno']!="":
        trip_no=get_nexttrain("077").find("Detail")['tripno']
        break
    time.sleep(1)

print()
print(trip_no)

station=""
while 1:
    res=xmltodict.parse(str(car_stat(trip_no).find("Detail")))["Detail"]
    if station!=res["@StationID"]:
        station=res["@StationID"]
        out[res["@StationID"]]=res
        print(station)

        f=open(str(trip_no),"w+")
        f.write(json.dumps(out))
        f.close()
        
    time.sleep(1)

    
