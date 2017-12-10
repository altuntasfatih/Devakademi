
from constant import TICK,description2,api
import requests,argparse,json,sys
import time
import threading

class Pricebot(threading.Thread):
    def __init__(self, number, sprice,bpirice):
        threading.Thread.__init__(self)
        self.sprice = float(sprice)
        self.bpirice = float(bpirice)
        self.num=number

    def stop(self):
        self.__stop = True

    def getData(self):
        re = None
        try:
            re = requests.get(TICK)
            if re.status_code == 200:
                j = json.loads(re.text)
                return j
        except Exception as e:
            pass
            return False

    def sendSms(self, message):
        result = api.call('sms.send', 'SMS', self.num, message, None)
        return result

    def check(self,value):
        stop = int(self.sprice)
        buy = int(self.bpirice)
        if value < stop and stop != -1:
            self.sendSms(self.number, "Your stop limit occurs current value is {} $".format(value))
            return 0
        elif abs(value - buy) < 3 and buy != -1:
            self.sendSms(self.number, "Your buy limit ocurs  current value is {} $".format(value))
            return 0
        return 1
    def run(self):
        prev = 0
        data = self.getData()
        print("Current value is {}".format(data['value']))

        if self.sprice != -1 and self.bpirice > data['value']:
            print("Stop limit can not lowwer than current Value")

        while True:
            data = self.getData()
            print("{} Current value is {}".format(self.name,data['value']))
            if data['date'] == prev:
                continue
            else:
                prev = data['date']
                if self.check(data['value'])==0:
                    break

            time.sleep(50)
            #link is updated 60 secodnds

