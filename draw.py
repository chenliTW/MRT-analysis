import matplotlib.pyplot as plt

import json

import sys


data=dict(json.loads(open(sys.argv[1],"r").read()))

x1 = [i for i in data]
car_1 = [float(data[i]["@Cart1W"]) for i in data]
car_2 = [float(data[i]["@Cart2W"]) for i in data]
car_3 = [float(data[i]["@Cart3W"]) for i in data]
car_4 = [float(data[i]["@Cart4W"]) for i in data]
car_5 = [float(data[i]["@Cart5W"]) for i in data]
car_6 = [float(data[i]["@Cart6W"]) for i in data]
#total = [ car_1[i]+car_2[i]+car_3[i]+car_4[i]+car_5[i] for i in range(22)]

#plt.plot(x1, total, 'b', label='sum')

plt.plot(x1, car_1, 'g', label='1')
plt.plot(x1, car_2, 'r', label='2')
plt.plot(x1, car_3, 'c', label='3')
plt.plot(x1, car_4, 'm', label='4')
plt.plot(x1, car_5, 'y', label='5')
plt.plot(x1, car_6, 'b', label='6')
plt.title(data[x1[0]]["@updateTime"])
plt.legend()
plt.savefig('{}.png'.format(data[x1[0]]["@updateTime"]))
