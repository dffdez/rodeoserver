import pushNotifications as ps
import database_api as db



# This functions checks favourites user's stocks in database and send notification
# if it's subscribed to that value.

# {'AAPL': {'price': '227.78999', 'state': '0'}, 'MSFT': {'price': '227.78999', 'state': '0'}}

def notificationManager(valuesState):

    valuesToNotify = {
        'ENT': [],
        'ENTAPX': [],
        'STP': [],
        'STPAPX': [],
        'SSL': [],
        'SSLAPX': [],
    }


    for stock, info in valuesState.items():
        state = info['state']

        if state == 'ENT':
            valuesToNotify['ENT'].append(stock)
        if state == 'ENTAPX':
            valuesToNotify['ENTAPX'].append(stock)
        if state == 'STP':
            valuesToNotify['STP'].append(stock)
        if state == 'STPAPX':
            valuesToNotify['STPAPX'].append(stock)
        if state == 'SSL':
            valuesToNotify['SSL'].append(stock)
        if state == 'SSLAPX':
            valuesToNotify['SSLAPX'].append(stock)

    
    for state, stocks in valuesToNotify.items():
        for stock in stocks:
            aliasToNotify = db.getTokenByFavourite(stock)
            for token in aliasToNotify:
                ps.send_push_message(token[0], [state, stock])



# Para pruebas

#notificationManager({'AAPL': {'price': '227.78999', 'state': 'ENT'}, 'MSFT': {'price': '227.78999', 'state': '0'}})