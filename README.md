# Devakademi
This is a workshop project in dev.akademi (sahibinden),
* bot.py        : It  is a bot for Scoin to check BUY or STOP-LIMIT orders.It takes orders and user telephone number from consoles.Then  bot checks  current price of Scoin regularly ,if  the price is triggered orders,bot informs user by  sending sms.İf there may  be  Api for Scoin ,this bot  can automatically performs orders like as  other coin stock market 
* constant.py   : Constant declaration
* predictor.py  : This is console script which performs  predictions.It predict next days price of Scoin using Linear regression model learning from  history data.In addition.İt shows graph of last two week of prices.
* predict.py    : This is only  modified  state of predictor.py to be able work  on restApı.py
* pricebot.py   : This is only  modified  state of bot.py to be able work  on restApı.py.
* restApi.py    : This is basic restful web service.İt supports '/predict'  and '/bot'

- GET /predict?day=3  : Estimating  price of Scoin  for after 3 days 
- GET /predict?days=5 : Estimating  price ofScoin  for the next 5 days

- POST /bot 
'{"num":"+905346639019", "sprice": "14550.0","bpirice":"-1"}'
          :With this request apı create a object(thread object)  from pricebot.py and seting attribute of object  from  post data,then start threads,İf prices of Scoin  intersect orders,sending sms users


