from websocket import create_connection
import socketio
import requests
import json
import time as times
from datetime import datetime, time
import pytz

import database_api as db
import notificationManager as nm

# API key de TwelveData
from apikey import APIKEY, APIKEYDEMO

IP_SERVER = 'rodeo_server'
PORT_SERVER = '5000'


spain_tz = pytz.timezone("Europe/Madrid")
start_time = time(15, 30)
end_time = time(20, 00)


def jsonMaker(symbol, price, state):
    response = {
        "price": price,
        "state": state        
    }

    return response

def jsonMakerFront(symbol, price, state, datetime, change, percent_change):
    response = {
        "price": price,
        "state": state,
        "datetime": datetime,
        "change": change,
        "percent_change": percent_change,
    }

    return response

def checkRefLimits(stock, rsi_1m, rsi_5m, stoch_1m, stoch_5m):

    limits = db.getLimitsRef(stock)

    e_apx_rsi_min = float(limits[1])
    e_apx_rsi_max = float(limits[2])
    e_apx_stoch_min = float(limits[3])
    e_apx_stoch_max = float(limits[4])
    e_ent_rsi_min = float(limits[5])
    e_ent_rsi_max = float(limits[6])
    e_ent_stoch_min = float(limits[7])
    e_ent_stoch_max = float(limits[8])


    # ENTAPX limits
    apx_rsi_min = min(e_apx_rsi_min, e_ent_rsi_min)
    apx_rsi_max = max(e_apx_rsi_max, e_ent_rsi_max)
    apx_stoch_min = min(e_apx_stoch_min, e_ent_stoch_min)
    apx_stoch_max = max(e_apx_stoch_max, e_ent_stoch_max)

   
    # ENTRADA 
    if (rsi_1m > e_ent_rsi_min and rsi_1m < e_ent_rsi_max and rsi_5m > e_ent_rsi_min and rsi_5m < e_ent_rsi_max and 
        stoch_1m > e_ent_stoch_min and stoch_1m < e_ent_stoch_max and stoch_5m > e_ent_stoch_min and stoch_5m < e_ent_stoch_max):
        db.setState(stock, 'ENT')
        return 'ENT'
    
    # ENTRADA APROXIMACION
    if (rsi_1m > apx_rsi_min and rsi_1m < apx_rsi_max and rsi_5m > apx_rsi_min and rsi_5m < apx_rsi_max and 
        stoch_1m > apx_stoch_min and stoch_1m < apx_stoch_max and stoch_5m > apx_stoch_min and stoch_5m < apx_stoch_max):
        return 'ENTAPX'
    
    return '0'
    



def checkLimits(stock, estado, valor_actual, valor_entrada, tiemposalida, rsi_1m, rsi_5m, stoch_1m, stoch_5m, ref_state):

    limits = db.getLimits(stock)

    e_apx_rsi_min = float(limits[1])
    e_apx_rsi_max = float(limits[2])
    e_apx_stoch_min = float(limits[3])
    e_apx_stoch_max = float(limits[4])
    e_ent_rsi_min = float(limits[5])
    e_ent_rsi_max = float(limits[6])
    e_ent_stoch_min = float(limits[7])
    e_ent_stoch_max = float(limits[8])
    stp_apx_stoch_min = float(limits[9])
    stp_apx_stoch_max = float(limits[10])
    stp_sal_stoch_min = float(limits[11])
    ssl_apx_value_min = float(limits[12])
    ssl_apx_value_max = float(limits[13])
    ssl_sal_value_min = float(limits[14])



    # ENTAPX limits
    apx_rsi_min = min(e_apx_rsi_min, e_ent_rsi_min)
    apx_rsi_max = max(e_apx_rsi_max, e_ent_rsi_max)
    apx_stoch_min = min(e_apx_stoch_min, e_ent_stoch_min)
    apx_stoch_max = max(e_apx_stoch_max, e_ent_stoch_max)

    # SSL limits
    ssl_min = valor_actual*(ssl_apx_value_min/100)
    ssl_max = valor_actual*(ssl_apx_value_max/100)

    ssl_sal = valor_actual*(ssl_sal_value_min/100)



    if estado == '0' or estado == 'ENTAPX':

        # ENTRADA 
        if (rsi_1m > e_ent_rsi_min and rsi_1m < e_ent_rsi_max and rsi_5m > e_ent_rsi_min and rsi_5m < e_ent_rsi_max and 
            stoch_1m > e_ent_stoch_min and stoch_1m < e_ent_stoch_max and stoch_5m > e_ent_stoch_min and stoch_5m < e_ent_stoch_max and ref_state == 'ENT'):
            db.setState(stock, 'ENT')
            db.setValorEntrada(stock, valor_actual)
            return 'ENT'
        
        # ENTRADA APROXIMACION
        if (rsi_1m > apx_rsi_min and rsi_1m < apx_rsi_max and rsi_5m > apx_rsi_min and rsi_5m < apx_rsi_max and 
            stoch_1m > apx_stoch_min and stoch_1m < apx_stoch_max and stoch_5m > apx_stoch_min and stoch_5m < apx_stoch_max and (ref_state == 'ENT' or ref_state == 'ENTAPX')):
            db.setState(stock, 'ENTAPX')
            return 'ENTAPX'
        
    

    elif estado == 'ENT' or estado == 'STPAPX':


        # SALIDA TAKE PROFIT
        if (stoch_1m > stp_sal_stoch_min and stoch_5m > stp_sal_stoch_min):
            db.setState(stock, 'STP')
            return 'STP'
        

        # SALIDA TAKE PROFIT APROXIMACION
        if (stoch_1m > stp_apx_stoch_min and stoch_1m < stp_apx_stoch_max and stoch_5m > stp_apx_stoch_min and stoch_5m < stp_apx_stoch_max):
            db.setState(stock, 'STPAPX')
            return 'STPAPX'
        

        
    
    elif estado == 'STP' or estado == 'SSLAPX' :

        # SALIDA STOP LESS APROXIMACION
        if (valor_entrada < ssl_min and valor_entrada > ssl_max):
            db.setState(stock, 'SSLAPX')
            return 'SSLAPX'
        
        # SALIDA STOP LESS
        if (valor_entrada <= ssl_sal):
            db.setState(stock, 'SSL')
            #time = time.time()
            db.setTiempoSalida(stock, times.time())
            return 'SSL'
        
        

    elif estado == 'SSL':
        difTime = times.time() - float(tiemposalida)
        
        # MANTENER SALIDA STOP LESS

        #Configurar tiempo
        #if (difTime >= x):


        if (difTime >= 60):
            db.setState(stock, '00')
            db.setTiempoSalida(stock, times.time())
            return '00'
        

    elif estado == '00':
        difTime = times.time() - float(tiemposalida)
        
        # NUEVO COMIENZO

        #Configurar tiempo
        #if (difTime >= x):
        #print(difTime)

        if (difTime >= 600):
            db.setState(stock, '0')
            db.setTiempoSalida(stock, 0)
            return '0'
        
        
        
   ##
   ##
   ## Si en la app no se manda estado nuevo mantener lo que hay









# WEBSOCKETS para comunicar con el servidor principal // Esto va en contenedor aparte
http_session = requests.Session()
http_session.verify = False
ws = socketio.Client(http_session=http_session)
#ws = socketio.Client()

ws.connect("wss://"+IP_SERVER+":"+PORT_SERVER, namespaces=['/stocks'])



# Para pruebas
i = 0
state = ['0', 'ENT', 'ENTAPX', 'STP', 'STPAPX', 'SSL', 'SSLAPX']
price = 100



while True:

    current_time = datetime.now(spain_tz).time()


    if start_time <= current_time <= end_time:

        semaforo = db.getStoplight()

        semaforodict = {
            "0": semaforo[0],
            "00": semaforo[0],
            "ENT": semaforo[1],
            "ENTAPX": semaforo[2],
            "STP": semaforo[3],
            "STPAPX": semaforo[4],
            "SSL": semaforo[5],
            "SSLAPX": semaforo[6]
        }

        response = {}
        responseNotification = {}

        # Nasdaq reference
        url_nasdaq_rsi_1m = "https://api.twelvedata.com/rsi?symbol=NDAQ&outputsize=1&interval=1min&apikey="+APIKEY
        url_nasdaq_rsi_5m = "https://api.twelvedata.com/rsi?symbol=NDAQ&outputsize=1&interval=5min&apikey="+APIKEY

        url_nasdaq_stoch_1m = "https://api.twelvedata.com/stoch?symbol=NDAQ&outputsize=1&interval=1min&apikey="+APIKEY
        url_nasdaq_stoch_5m = "https://api.twelvedata.com/stoch?symbol=NDAQ&outputsize=1&interval=5min&apikey="+APIKEY

        result_nasdaq_rsi_1m = requests.get(url_nasdaq_rsi_1m).content.decode('utf-8')
        result_nasdaq_rsi_5m = requests.get(url_nasdaq_rsi_5m).content.decode('utf-8')
        result_nasdaq_stoch_1m = requests.get(url_nasdaq_stoch_1m).content.decode('utf-8')
        result_nasdaq_stoch_5m = requests.get(url_nasdaq_stoch_5m).content.decode('utf-8')

        print(result_nasdaq_rsi_1m)

        nasdaq_rsi_1m = float(json.loads(result_nasdaq_rsi_1m)['values'][0]['rsi'])
        nasdaq_rsi_5m = float(json.loads(result_nasdaq_rsi_5m)['values'][0]['rsi'])
        nasdaq_stoch_1m = float(json.loads(result_nasdaq_stoch_1m)['values'][0]['slow_k'])
        nasdaq_stoch_5m = float(json.loads(result_nasdaq_stoch_5m)['values'][0]['slow_k'])

        print(result_nasdaq_rsi_1m)


        # Bitcoin reference
        """ url_bitcoin_rsi_1m = "https://api.twelvedata.com/rsi?symbol=BTC/USD&outputsize=1&interval=1min&apikey="+APIKEY
        url_bitcoin_rsi_5m = "https://api.twelvedata.com/rsi?symbol=BTC/USD&outputsize=1&interval=5min&apikey="+APIKEY

        url_bitcoin_stoch_1m = "https://api.twelvedata.com/stoch?symbol=BTC/USD&outputsize=1&interval=1min&apikey="+APIKEY
        url_bitcoin_stoch_5m = "https://api.twelvedata.com/stoch?symbol=BTC/USD&outputsize=1&interval=5min&apikey="+APIKEY

        result_bitcoin_rsi_1m = requests.get(url_bitcoin_rsi_1m).content.decode('utf-8')
        result_bitcoin_rsi_5m = requests.get(url_bitcoin_rsi_5m).content.decode('utf-8')

        result_bitcoin_stoch_1m = requests.get(url_bitcoin_stoch_1m).content.decode('utf-8')
        result_bitcoin_stoch_5m = requests.get(url_bitcoin_stoch_5m).content.decode('utf-8')

        bitcoin_rsi_1m = float(json.loads(result_bitcoin_rsi_1m)['values'][0]['rsi'])
        bitcoin_rsi_5m = float(json.loads(result_bitcoin_rsi_5m)['values'][0]['rsi'])
        bitcoin_stoch_1m = float(json.loads(result_bitcoin_stoch_1m)['values'][0]['slow_k'])
        bitcoin_stoch_5m = float(json.loads(result_bitcoin_stoch_5m)['values'][0]['slow_k'])
        """


        nasdaq_state = checkRefLimits("NDAQ", nasdaq_rsi_1m, nasdaq_rsi_5m, nasdaq_stoch_1m, nasdaq_stoch_5m)
        #bitcoin_state = checkRefLimits("BTC", bitcoin_rsi_1m, bitcoin_rsi_5m, bitcoin_stoch_1m, bitcoin_stoch_5m)

        

        for index, stock in enumerate(db.getStocksName()):

            # INFO

            url_price = "https://api.twelvedata.com/price?symbol="+stock[0]+"&apikey="+APIKEYDEMO
            result_price = requests.get(url_price).content.decode('utf-8')
            data_price = json.loads(result_price)['price']

            url_quote = "https://api.twelvedata.com/quote?symbol="+stock[0]+"&interval=1min&apikey="+APIKEYDEMO
            result_quote = requests.get(url_quote).content.decode('utf-8')
            data_quote_time = json.loads(result_quote)['datetime']
            data_quote_change = json.loads(result_quote)['change']
            data_quote_percent = json.loads(result_quote)['percent_change']



            # RSI y STOCH

            url_rsi_1m = "https://api.twelvedata.com/rsi?symbol="+stock[0]+"&outputsize=1&interval=1min&apikey="+APIKEYDEMO
            url_rsi_5m = "https://api.twelvedata.com/rsi?symbol="+stock[0]+"&outputsize=1&interval=5min&apikey="+APIKEYDEMO
            url_stoch_1m = "https://api.twelvedata.com/stoch?symbol="+stock[0]+"&outputsize=1&interval=1min&apikey="+APIKEYDEMO
            url_stoch_5m = "https://api.twelvedata.com/stoch?symbol="+stock[0]+"&outputsize=1&interval=5min&apikey="+APIKEYDEMO

            result_rsi_1m = requests.get(url_rsi_1m).content.decode('utf-8')
            result_rsi_5m = requests.get(url_rsi_5m).content.decode('utf-8')
            result_stoch_1m = requests.get(url_stoch_1m).content.decode('utf-8')
            result_stoch_5m = requests.get(url_stoch_5m).content.decode('utf-8')

            value_rsi_1m = float(json.loads(result_rsi_1m)['values'][0]['rsi'])
            value_rsi_5m = float(json.loads(result_rsi_5m)['values'][0]['rsi'])
            value_stoch_1m = float(json.loads(result_stoch_1m)['values'][0]['slow_k'])
            value_stoch_5m = float(json.loads(result_stoch_5m)['values'][0]['slow_k'])

            # Comprueba los límites en función de si es accion o crypto
            if (stock[2] == 'A'):
                value_state = checkLimits(stock[0], stock[1], float(data_price), stock[3], stock[4], value_rsi_1m, value_rsi_5m, value_stoch_1m, value_stoch_5m, nasdaq_state)
            elif (stock[2] == 'C'):
                #value_state = checkLimits(stock[0], stock[1], float(data_price), stock[3], stock[4], value_rsi_1m, value_rsi_5m, value_stoch_1m, value_stoch_5m, bitcoin_state)
                continue

            #print(value_state)

            responseNotification[stock[0]] = jsonMaker(stock[0], data_price, value_state)
            response[stock[0]] = jsonMakerFront(stock[0], data_price, semaforodict[stock[1]], data_quote_time, data_quote_change, data_quote_percent)


        #print(response)


        nm.notificationManager(responseNotification)
        ws.send(response, namespace='/stocks')
        

        # Configurable
        times.sleep(80)

    
    else:

        semaforo = db.getStoplight()
        #print(semaforo)

        semaforodict = {
            "0": semaforo[0],
            "ENT": semaforo[1],
            "ENTAPX": semaforo[2],
            "STP": semaforo[3],
            "STPAPX": semaforo[4],
            "SSL": semaforo[5],
            "SSLAPX": semaforo[6]
        }

        response = {'AAPL': {'price': str(price), 'state': semaforodict[state[i]], 'datetime': '10-09-2024', 'change': '0.005', 'percent_change': '0.01%'}}
        responseNotification = {'AAPL': {'price': str(price), 'state': state[i], 'datetime': '10-09-2024', 'change': '0.005', 'percent_change': '0.01%'}}

        ws.send(response, namespace='/stocks')
        #nm.notificationManager(responseNotification)


        i += 1
        price += 1
        if price >= 250:
            price = 100
        if i == len(state):
            i = 0
        
        # Configurable
        times.sleep(1)


