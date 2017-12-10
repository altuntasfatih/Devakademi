import requests,sys,datetime,json,argparse
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from constant import HIST,TICK,description
import matplotlib.pyplot as plt


HISTORY=None
Dates=[]
Prices=[]

parser = argparse.ArgumentParser("Predictor dev.akademi", description)
parser.add_argument("--day", "-d", help="How many day laters", required=False, default=1)
parser.add_argument("--days", "-ds", help="How many days to next?", required=False, default=-1)
args = parser.parse_args()


def getPage(url):
    re = None
    try:
        re = requests.get(url)
        if re.status_code == 200:
            j = json.loads(re.text)
            return  j
    except Exception as e:
        pass
        return False

def update():
    global Dates, Prices
    current=getPage(TICK)
    zero = round(HISTORY[0]['date'] / (1000 * 60 * 60))
    tm = round(current['date'] / (1000 * 60 * 60)) - zero
    Dates.append(tm)
    Prices.append(current['value'])

    return current


def getHist():
    global HISTORY
    HISTORY = getPage(HIST)


def predict_price(x):
    global Dates,Prices


    date_l = Dates[-15:]
    prices_l = Prices[-15:]


    dates_np = np.reshape(date_l, (len(date_l), 1))
    last=date_l[len(date_l)-1]
    x = x + last
    svr_rbf = SVR(kernel='rbf')

    svr_rbf.fit(dates_np, prices_l)

    return  svr_rbf.predict(x)[0]


def predict_price_Linear(x):
    global Dates
    global Prices
    date_l = Dates[-15:]
    prices_l= Prices[-15:]


    dates_np = np.reshape(date_l, (len(date_l), 1))

    last = date_l[len(date_l) - 1]
    x = x + last

    linridge = Ridge().fit(dates_np, prices_l)
    return linridge.predict(x)[0]


def sentize():
    global Prices,Dates
    #datalar gunluk
    #1096 is duplicate day,
    dates = []
    prices = []
    zero=round(HISTORY[0]['date']/(1000*60*60))#second,minute,hour
    for item in HISTORY:
        tm=round(item['date']/(1000*60*60))-zero
        tm=round(tm/24)#day
        dates.append(tm)
        prices.append(item['value'])


    d = {x: dates.count(x) for x in dates}
    index=0
    for key, value in d.items():
        if value==1:
            Dates.append(key)
            Prices.append(prices[index])
        elif value!=1:

            avverage=0;
            for i in range(index,index+value):
                avverage=avverage+prices[index]
                index+=1
            avverage=(avverage/value)
            Dates.append(key)
            Prices.append(avverage)
        index+=1


def plot():
    x = Dates[-14:]
    y = Prices[-14:]
    x = list(map(lambda b: b - (min(x)-1), x))


    plt.figure()
    plt.plot(x, y, 'g',label='Scoin')
    plt.title('Last 15 days situation')
    plt.legend()
    plt.show()

def start():

    getHist()
    sentize()
    if args.days!=-1:
        for i in range(1,int(args.days),1):
            #print("Result SVM   in next {} day -> {}$".format(i,predict_price(i)))
            print("Result ridge in next {} day -> {}$".format(i,predict_price_Linear(i)))

    else:
        #print("Result SVM   -> {}$".format(predict_price(int(args.day))))
        print("Result by ridge -> {}$".format(predict_price_Linear(int(args.day))))
    plot()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print (parser.print_help())
        exit()

    start()

