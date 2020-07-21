from flask import Flask,render_template,redirect,url_for
import os
from datetime import datetime
import base64

app=Flask(__name__)

def allow_list(line,dir):
    line_list=["BL"]
    dir_list=["eastbound","westbound"]
    assert line in line_list
    assert dir in dir_list 

def list_image(line,dir,date):
    allow_list(line,dir)
    try:
        res=os.listdir("./data/{}/{}/{}/json/".format(line,date,dir))
    except:
        res=[]
    res=[i.replace(".json","") for i in res]
    return sorted(res)

@app.route("/")
def index():
    return redirect("https://mrt.le37.tw/BL/eastbound/")
    
@app.route("/<line>/<dir>/")
def section_index(line,dir):
    allow_list(line,dir)
    date=datetime.now().strftime("%Y-%m-%d")
    return redirect("https://mrt.le37.tw/"+line+"/"+dir+"/"+date+"/")

@app.route("/<line>/<dir>/<date>/")
def show(line,dir,date):
    allow_list(line,dir)
    datetime.strptime(date, "%Y-%m-%d")
    trip=list_image(line,dir,date)
    return render_template("index.html",date=date,trip=trip,img="",info=line+" "+dir,json="")

@app.route("/<line>/<dir>/<date>/<time>")
def getimg(line,dir,date,time):
    allow_list(line,dir)
    datetime.strptime(date, "%Y-%m-%d")
    datetime.strptime(time, "%H:%M:%S")
    trip=list_image(line,dir,date)
    return render_template("index.html",time=time,date=date,trip=trip,info=line+" "+dir,json=str(base64.b64encode(open("./data/{}/{}/{}/json/{}.json".format(line,date,dir,time),"rb").read()))[2:-1])

@app.route("/dateselect/")
def dateselect():
    return render_template("date.html")

app.run(port=9000)


