import requests
from bs4 import BeautifulSoup
import time
import datetime
import xmltodict
import json
import os
from multiprocessing import Process

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


def job(trip_no):
    out={}
    station=""
    retry_cnt=0
    x1 = [i for i in out]
    while 1:
        try:
            res=xmltodict.parse(str(car_stat(trip_no).find("Detail")))["Detail"]
            retry_cnt=0
            if station!=res["@StationID"]:
                station=res["@StationID"]
                out[res["@StationID"]]=res
                x1 = [i for i in out]
                print(trip_no,station)
                if x1[0]!="BL23":
                    return
                os.makedirs("./data/BL/{}/westbound/json/".format(out[x1[0]]["@updateTime"].split(" ")[0]), exist_ok=True)
                f=open("data/BL/{}/westbound/json/{}.json".format(out[x1[0]]["@updateTime"].split(" ")[0],out[x1[0]]["@updateTime"].split(" ")[1]),"w+")
                f.write(json.dumps(out))
                f.close()
                if station=="BL01":
                    break            
            time.sleep(5)
        except:
            if retry_cnt>=10:
                if len(x1)>0:
                    print("LOST{}".format(trip_no))
                    os.remove("data/BL/{}/westbound/json/{}.json".format(out[x1[0]]["@updateTime"].split(" ")[0],out[x1[0]]["@updateTime"].split(" ")[1]))
                return
            retry_cnt+=1
            time.sleep(1)

    #os.system("/usr/bin/python3.7 draw_rev.py data/BL/{}/westbound/json/{}.json".format(out[x1[0]]["@updateTime"].split(" ")[0],out[x1[0]]["@updateTime"].split(" ")[1]))
    return 

if __name__=="__main__":
    trip_no=""
    tmp=""
    process_list = []
    while 1:
        if datetime.datetime.now().hour==2:
            break

        while 1:
            try:
                #print(get_nexttrain("077").find("Detail"))
                if get_nexttrain("097").find_all("Detail")[1]['tripno']!="":
                    trip_no=get_nexttrain("097").find_all("Detail")[1]['tripno']
                    break
            except:
                pass
            time.sleep(2)

        if trip_no!=tmp:
            print(trip_no)
            p=Process(target=job,args=(trip_no,))
            p.start()
            process_list.append(p)
            tmp=trip_no
        time.sleep(5)

    for process in process_list:
         process.join()

    
