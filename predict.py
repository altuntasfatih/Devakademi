import requests,sys,datetime,json,argparse
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from constant import HIST,TICK,description



HISTORY=None
Dates=[]
Prices=[]


class Predict():

    def getPage(self):
        re = None
        try:
            re = requests.get(HIST)
            if re.status_code == 200:
                j = json.loads(re.text)
                return j
        except Exception as e:
            pass
            return False

    def getHist(self):
        global HISTORY
        HISTORY = self.getPage()

    def predict_price(self,x):
        global Dates, Prices

        date_l = Dates[-15:]
        prices_l = Prices[-15:]

        dates_np = np.reshape(date_l, (len(date_l), 1))
        last = date_l[len(date_l) - 1]
        x = x + last
        svr_rbf = SVR(kernel='rbf')

        svr_rbf.fit(dates_np, prices_l)

        return svr_rbf.predict(x)[0]

    def predict_price_Linear(self,x):
        global Dates
        global Prices
        date_l = Dates[-15:]
        prices_l = Prices[-15:]

        dates_np = np.reshape(date_l, (len(date_l), 1))

        last = date_l[len(date_l) - 1]
        x = x + last

        linridge = Ridge().fit(dates_np, prices_l)
        return linridge.predict(x)[0]

    def sentize(self):
        global Prices, Dates
        # datalar gunluk
        # 1096 is duplicate day,
        dates = []
        prices = []
        zero = round(HISTORY[0]['date'] / (1000 * 60 * 60))  # second,minute,hour
        for item in HISTORY:
            tm = round(item['date'] / (1000 * 60 * 60)) - zero
            tm = round(tm / 24)  # day
            dates.append(tm)
            prices.append(item['value'])

        d = {x: dates.count(x) for x in dates}
        index = 0
        for key, value in d.items():
            if value == 1:
                Dates.append(key)
                Prices.append(prices[index])
            elif value != 1:

                avverage = 0;
                for i in range(index, index + value):
                    avverage = avverage + prices[index]
                    index += 1
                avverage = (avverage / value)
                Dates.append(key)
                Prices.append(avverage)
            index += 1

    def start(self,day,flag):

        self.getHist()
        self.sentize()
        result=[]
        if flag == 1:
            for i in range(1, int(day), 1):
                result.append("Result ridge in next {} day -> {}$".format(i, self.predict_price_Linear(i)))

        else:

            result.append("Result by ridge -> {}$".format(self.predict_price_Linear(int(day))))

        return result









