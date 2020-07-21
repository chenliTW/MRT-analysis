import matplotlib.pyplot as plt

import json

import sys


data=dict(json.loads(open(sys.argv[1],"r").read()))

x1 = [i for i in sorted(data.keys())]
x1 = x1[::-1]

if len(x1)!=23:
    exit(0)

car_1 = [float(data[i]["@Cart1W"]) for i in x1[1:]]
car_2 = [float(data[i]["@Cart2W"]) for i in x1[1:]]
car_3 = [float(data[i]["@Cart3W"]) for i in x1[1:]]
car_4 = [float(data[i]["@Cart4W"]) for i in x1[1:]]
car_5 = [float(data[i]["@Cart5W"]) for i in x1[1:]]
car_6 = [float(data[i]["@Cart6W"]) for i in x1[1:]]
total = [ (car_1[i]+car_2[i]+car_3[i]+car_4[i]+car_5[i]+car_6[i])/6  for i in range(22)]
x1=x1[:-1]
#plt.plot(x1, total, 'b', label='sum')





fig, ax1 = plt.subplots(figsize=(16,9))
ax1.set_xlabel('station')
ax1.set_ylabel('car weight', color="k")

ax1.plot(x1, car_1, 'g', label='1st car')
ax1.plot(x1, car_2, 'c', label='2nd car')
ax1.plot(x1, car_3, 'm', label='3rd car')
ax1.plot(x1, car_4, 'k', label='4th car')
ax1.plot(x1, car_5, 'tab:olive', label='5th car')
ax1.plot(x1, car_6, 'b', label='6th car')
ax1.legend(loc="upper left")

ax1.set_ylim([3,5.2])

ax2 = ax1.twinx()
ax2.set_ylabel('average weight', color="r")

ax2.plot(x1, total, color="r",linestyle=":",label="average weight",zorder=10)

ax2.legend(loc="upper right")
ax2.set_ylim([3,5.2])

plt.title(data[x1[0]]["@updateTime"])


import os
os.makedirs("./data/BL/{}/westbound/image/".format(data[x1[0]]["@updateTime"].split(" ")[0]), exist_ok=True)

plt.savefig('./data/BL/{}/westbound/image/{}.png'.format(data[x1[0]]["@updateTime"].split(" ")[0],data[x1[0]]["@updateTime"].split(" ")[1]))
