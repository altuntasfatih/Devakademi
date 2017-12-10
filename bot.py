
from constant import TICK,description2,api
import requests,argparse,json,sys
import time


parser = argparse.ArgumentParser("dev.akademi bot sell and buy scoin", description2)
parser.add_argument("--stoplimit", "-s", help="How many day laters", required=False, default=-1)
parser.add_argument("--buylimit", "-b", help="How many days to next?", required=False, default=-1)
parser.add_argument("--number", "-n", help="Which number to inform", required=False, default='+905346639019')
args = parser.parse_args()

def getData():
    re = None
    try:
        re = requests.get(TICK)
        if re.status_code == 200:
            j = json.loads(re.text)
            return  j
    except Exception as e:
        pass
        return False


def sendSms(number,message):
    result = api.call('sms.send', 'SMS', number, message, None)
    return result

def check(value):
    stop=int(args.stoplimit)
    buy =int(args.buylimit)
    if value < stop and  stop != -1:
        print("Your stop limit occurs current value is {} $".format(value))
        sendSms(args.number,"Your stop limit occurs current value is {} $".format(value))
        exit()
    elif abs(value -buy ) < 3  and buy != -1:
        print("Your stop limit occurs current value is {} $".format(value))
        sendSms(args.number, "Your buy limit ocurs  current value is {} $".format(value))
        exit()


def start():
    prev=0
    data = getData()
    print("Current value is {}".format(data['value']))

    if int(args.stoplimit) != -1 and int(args.stoplimit) > data['value']:
        print("Stop limit can not lowwer than current Value")

    while True:
        data=getData()
        #print("Current value is {}".format(data['value']))
        if data['date']==prev:
            continue
        else:
            prev=data['date']
            print("Current value is {}".format(data['value']))
            check(data['value'])







if __name__ == "__main__":

    if args.stoplimit==-1 and args.buylimit==-1:
        print("Parameters not entered")
    else:
        start()










