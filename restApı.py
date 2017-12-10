#!flask/bin/python
from flask import Flask, jsonify, request,abort
from  predict import Predict
from pricebot import Pricebot
import json

app = Flask(__name__)
priceThredlist=[]
temp=Predict()

@app.route('/', methods = ['POST'])
def start():
    abort(202)

@app.route('/bot', methods = ['POST'])
def bot():
    if not request.json:
        abort(400)
    data=request.json

    #Thread is not neccesry here I know,but ı don't have time to change
    #one solution,new one thread always  check all users sprice and bprice,then send sms specific user
    #new solution is more economic :)
    
    th=Pricebot(number=data['num'],sprice=data['sprice'],bpirice=data['bpirice'])
    th.start()
    priceThredlist.append(th)
    return "Bot is stared <br>"

@app.route('/predict', methods=['GET'])
def predict():

    days = request.args.get('days')
    day = request.args.get('day')

    result=None

    if day==None and days==None:
        result=temp.start(1,0)
    elif day==None:
        result = temp.start(int(days), 1)
    elif days == None:
        result = temp.start(int(day), 0)

    string = ''
    for item in result:
        string = string +item+ '<br>'
    return  string

if __name__ == '__main__':
     app.run(port='5002')

#curl -i -H "Content-Type: application/json" -X POST -d  '{"num":"+905346639019", "sprice": "14550.0","bpirice":"-1"}' http://localhost:5002/bot