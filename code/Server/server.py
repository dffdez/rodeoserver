from flask import Flask, request, jsonify, make_response, session, send_from_directory, Response, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit, send, join_room, leave_room, rooms
from functools import wraps
from datetime import timedelta
import os
import requests
import json

import database_api as db

# API key de TwelveData
from apikey import APIKEY, APIKEYDEMO

IMAGE_FOLDER = 'media/articles/'
VIDEO_FOLDER = 'media/video/'
DOCUMENT_FOLDER = 'media/documents/'

IMAGE_FOLDER_ICON = 'media/icons/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
socketio = SocketIO(app)

app.config['UPLOAD_FOLDER_IMAGES'] = IMAGE_FOLDER
app.config['UPLOAD_FOLDER_VIDEO'] = VIDEO_FOLDER
app.config['UPLOAD_FOLDER_DOCUMENTS'] = DOCUMENT_FOLDER

app.config['UPLOAD_FOLDER_ICON'] = IMAGE_FOLDER_ICON

app.config['SECRET_KEY'] = '959fec02412248ebbdfd23a96eeafa73'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=6)
jwt = JWTManager(app)



##
## PETICIONES PARA LOGIN Y REGISTRO
##


# login permite acceder a la aplicacion a usuarios registrados

@app.route('/login', methods=['POST'])
def login():

    #Peticion en formato JSON
    auth = request.json

    #Lectura de credenciales de la peticion
    username = auth['username']
    password = auth['password']


    try:
        credentials = db.login(username, password)
        print(username)
        print(credentials)
        

        if credentials:
        
            if username != credentials[0] or password != credentials[1]:
                return jsonify({'message': 'Invalid credentials'}), 401
            else:
                #Si el usuario es administrador se añade el parametro admin
                if (credentials[2]):
                    access_token = create_access_token(identity=username)
                    print('access_token admin')
                    print(access_token)
                    return jsonify(access_token=access_token, admin='admin'), 200
                else:
                    access_token = create_access_token(identity=username)
                    print('access_token')
                    print(access_token)
                    return jsonify(access_token=access_token), 200
                
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except:
        return jsonify({'message': 'Error'}), 500
    



# signup permite el registro de nuevos usuarios

@app.route('/signup', methods=['POST'])
def signup():

    data = request.json

    
    alias = data['alias']
    name = data['name']
    surname = data['surname']
    email = data['email']
    password = data['password']

    
    result = db.addNewUser(alias, password, name, surname, email)
        
    if result == True:
        return jsonify({'message': 'OK'}), 200
    else:
        return jsonify({'message': 'Error'}), 500


# signup permite el registro de nuevos usuarios

@jwt_required()
@app.route('/signupAdmin', methods=['POST'])
def signupAdmin():

    data = request.json

    
    alias = data['alias']
    name = data['name']
    surname = data['surname']
    email = data['email']
    password = data['password']

    
    result = db.addNewAdmin(alias, password, name, surname, email)
        
    if result == True:
        return jsonify({'message': 'OK'}), 200
    else:
        return jsonify({'message': 'Error'}), 500



# setPushNotificationToken permite el registro de nuevos usuarios para notificaciones

@app.route('/setPushNotificationToken', methods=['POST'])
@jwt_required()
def setPushNotificationToken():

    data = request.json

    alias = data['alias']
    token = data['token']
    
    db.setPushNotificationToken(alias, token)
        
    return jsonify(), 200

    

    # setPushNotificationToken permite el registro de nuevos usuarios

@app.route('/getPushNotificationToken', methods=['GET'])
@jwt_required()
def getPushNotificationToken():

    result = db.getPushNotificationToken()
        
    return jsonify(result), 200


    

##
## PETICIONES PARA OBTENER USUARIOS DE LA BASE DE DATOS
##


# getAllUser devuelve los alias de todos los usuarios

@app.route('/getAllUser', methods=['GET'])
@jwt_required()
def getAllUser():

    users = db.getAllUser()

    return jsonify(users), 200



# getUserInfo devuelve la informacion de un usuario de la base de datos

@app.route('/getUserInfo', methods=['POST'])
@jwt_required()
def getUserInfo():

    data = request.json

    alias = data['alias']


    userinfo = db.getUser(alias)

    return jsonify(userinfo), 200



# deleteUser devuelve la informacion de un usuario de la base de datos

@app.route('/deleteUser', methods=['POST'])
@jwt_required()
def deleteUser():

    data = request.json
    alias = data['alias']
    db.deleteUser(alias)

    return jsonify(), 200


# changePassword modifica la contrasenia de un usuario de la base de datos

@app.route('/changePassword', methods=['POST'])
@jwt_required()
def changePassword():

    data = request.json

    alias = data['alias']
    password = data['password']
    db.modifyUserPass(alias, password)

    return jsonify(), 200


# changeUserData modifica la informacion de un usuario de la base de datos

@app.route('/changeUserData', methods=['POST'])
@jwt_required()
def changeUserData():

    data = request.json

    alias = data['alias']
    name = data['name']
    surname = data['surname']
    email = data['email']

    db.modifyUserData(alias, name, surname, email)

    return jsonify(), 200





##
## PETICIONES PARA OBTENER VALORES DE LA BASE DE DATOS
##


# getStocks devuelve todos los valores/cryptos de la base de datos

@app.route('/getStocks', methods=['GET'])
@jwt_required()
def getStocks():


    stocks = db.getStocks()

    return jsonify(stocks), 200


# getStocksFav devuelve todos los valores/cryptos de la base de datos marcando favoritos de usuario

@app.route('/getStocksFav', methods=['POST'])
@jwt_required()
def getStocksFav():
        
    data = request.json
    alias = data['alias']
    favourites = db.getFavourites(alias)  
    stocks = db.getStocks()
    result = []

    for i in stocks:
        if (i in favourites):
            result.append([i, True])
        else:
            result.append([i, False])


    return jsonify(result), 200

# getStocksFav devuelve todos los valores/cryptos de la base de datos marcando favoritos de usuario

@app.route('/getStocksFavStocks', methods=['POST'])
@jwt_required()
def getStocksFavStocks():
        
    data = request.json
    alias = data['alias']
    favourites = db.getFavourites(alias)  
    stocks = db.getStocks()
    result = []

    for i in stocks:

        if i[2] == 'A':
            if (i in favourites):
                result.append([i, True])
            else:
                result.append([i, False])


    return jsonify(result), 200

# getStocksFav devuelve todos los valores/cryptos de la base de datos marcando favoritos de usuario

@app.route('/getStocksFavCrypto', methods=['POST'])
@jwt_required()
def getStocksFavCrypto():
        
    data = request.json
    alias = data['alias']
    favourites = db.getFavourites(alias)  
    stocks = db.getStocks()
    result = []

    for i in stocks:

        if i[2] == 'C':
            if (i in favourites):
                result.append([i, True])
            else:
                result.append([i, False])


    return jsonify(result), 200




# getFavourites devuelve las acciones favoritas de un usuario

@app.route('/getFavourites', methods=['POST'])
@jwt_required()
def getFavourites():

    data = request.json

    alias = data['alias']
    favourites = db.getFavourites(alias)  

    return jsonify(favourites), 200



# setFavourite devuelve las acciones favoritas de un usuario

@app.route('/setFavourite', methods=['POST'])
@jwt_required()
def setFavourite():

    data = request.json

    alias = data['alias']
    simbolo = data['simbolo']

    db.setFavourite(alias, simbolo)

    return jsonify(), 200


# deleteFavourite devuelve las acciones favoritas de un usuario

@app.route('/deleteFavourite', methods=['POST'])
@jwt_required()
def deleteFavourite():

    data = request.json

    alias = data['alias']
    simbolo = data['simbolo']

    db.deleteFavourite(alias, simbolo)

    return jsonify(), 200


# verifySymbol comprueba que el símbolo introducido es correcto

@app.route('/verifySymbol', methods=['POST'])
@jwt_required()
def verifySymbol():

    data = request.json

    simbolo = data['symbol']

    url = "https://api.twelvedata.com/quote?symbol="+simbolo+"&apikey="+APIKEY
    
    result = requests.get(url).content.decode('utf-8')
    data = json.loads(result)

    response = False
    if 'code' in data:
        response = False
    if 'symbol' in data :
        response = True

    print(response)

    return jsonify(response), 200


# newStock añade una nueva accion/crypto a la base de datos

@app.route('/newStock', methods=['POST'])
@jwt_required()
def newStock():

    data = request.json

    simbolo = data['symbol']
    nombre = data['name']
    ac = data['acselector']

    db.addNewStock(simbolo, nombre, ac)

    return jsonify(), 200


# newImage almacena un imagen en el servidor

@app.route('/newIconStock', methods=['GET', 'POST'])
@jwt_required()
def newIconStock():

    print(request.files)


    file = request.files['image']
    print(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER_ICON'], file.filename))


    return jsonify(), 200


# getImage devuelve imagenes almacenadas 

@app.route('/getIconStock/<name>', methods=['GET'])
@jwt_required()
def getIconStock(name):

    file = name+'.jpg'
   
    return send_from_directory(app.config['UPLOAD_FOLDER_ICON'], file), 200

# deleteStock elimina una accion/crypto a la base de datos

@app.route('/deleteStock', methods=['POST'])
@jwt_required()
def deleteStock():

    data = request.json

    simbolo = data['symbol']
    db.deleteStock(simbolo)
    os.remove(IMAGE_FOLDER_ICON+simbolo+'.jpg')


    return jsonify(), 200



# Websocket stocks

@socketio.on('connect', namespace='/stocks')
def connect_stocks():
    print('Hola, conectado a stocks!')

@socketio.on('join', namespace='/stocks')
def join_stocks(alias):
    print('Conectado ' + alias)

@socketio.on('leave', namespace='/stocks')
def leave_stocks(alias):
    print('Desconectado ' + alias)


# Websocket message

@socketio.on('message', namespace='/stocks')
def message_stocks(data):

    send(message=data, broadcast=True)





##
## PETICIONES PARA OBTENER LIMITES DE LA BASE DE DATOS
##


# getLimits devuelve los limites de valores/cryptos de la base de datos

@app.route('/getLimits', methods=['POST'])
@jwt_required()
def getLimits():

    data = request.json

    simbolo = data['simbolo']
    limits = db.getLimits(simbolo)

    return jsonify(limits), 200



# setLimits almacena los limites para un valor/crypto determinado

@app.route('/setLimits', methods=['POST'])
@jwt_required()
def setLimits():

    data = request.json

    simbolo = data['simbolo']
    e_apx_rsi_min = data['e_ent_rsi_max']
    e_apx_rsi_max = data['e_apx_rsi_max']
    e_apx_stoch_min = data['e_ent_stoch_max']
    e_apx_stoch_max= data['e_apx_stoch_max']
    e_ent_rsi_min = data['e_ent_rsi_min']
    e_ent_rsi_max = data['e_ent_rsi_max']
    e_ent_stoch_min = data['e_ent_stoch_min']
    e_ent_stoch_max = data['e_ent_stoch_max']
    stp_apx_stoch_min = data['stp_apx_stoch_min']
    stp_apx_stoch_max = data['stp_apx_stoch_max']
    stp_sal_stoch_min = data['stp_apx_stoch_max']
    ssl_apx_value_min = data['ssl_apx_value_min']
    ssl_apx_value_max = data['ssl_apx_value_max']
    ssl_sal_value_min = data['ssl_apx_value_max']
    
    limits = db.setLimits(simbolo, e_apx_rsi_min, e_apx_rsi_max, e_apx_stoch_min, e_apx_stoch_max, e_ent_rsi_min,
                          e_ent_rsi_max, e_ent_stoch_min, e_ent_stoch_max, stp_apx_stoch_min, stp_apx_stoch_max, 
                          stp_sal_stoch_min, ssl_apx_value_min, ssl_apx_value_max, ssl_sal_value_min)


    return jsonify(), 200



# getLimits devuelve los limites de valores/cryptos de la base de datos

@app.route('/getLimitsRef', methods=['POST'])
@jwt_required()
def getLimitsRef():

    data = request.json

    simbolo = data['simbolo']
    limits = db.getLimitsRef(simbolo)

    return jsonify(limits), 200



# setLimits almacena los limites para un valor/crypto determinado

@app.route('/setLimitsRef', methods=['POST'])
@jwt_required()
def setLimitsRef():

    data = request.json

    simbolo = data['simbolo']
    e_apx_rsi_min = data['e_ent_rsi_max']
    e_apx_rsi_max = data['e_apx_rsi_max']
    e_apx_stoch_min = data['e_ent_stoch_max']
    e_apx_stoch_max= data['e_apx_stoch_max']
    e_ent_rsi_min = data['e_ent_rsi_min']
    e_ent_rsi_max = data['e_ent_rsi_max']
    e_ent_stoch_min = data['e_ent_stoch_min']
    e_ent_stoch_max = data['e_ent_stoch_max']
    stp_apx_stoch_min = data['stp_apx_stoch_min']
    stp_apx_stoch_max = data['stp_apx_stoch_max']
    stp_sal_stoch_min = data['stp_apx_stoch_max']
    ssl_apx_value_min = data['ssl_apx_value_min']
    ssl_apx_value_max = data['ssl_apx_value_max']
    ssl_sal_value_min = data['ssl_apx_value_max']
    
    limits = db.setLimitsRef(simbolo, e_apx_rsi_min, e_apx_rsi_max, e_apx_stoch_min, e_apx_stoch_max, e_ent_rsi_min,
                          e_ent_rsi_max, e_ent_stoch_min, e_ent_stoch_max, stp_apx_stoch_min, stp_apx_stoch_max, 
                          stp_sal_stoch_min, ssl_apx_value_min, ssl_apx_value_max, ssl_sal_value_min)


    return jsonify(), 200


##
## PETICIONES PARA OBTENER BLOG DE LA BASE DE DATOS
##


# getBlog devuelve todos los posts almacenados 

@app.route('/getPosts', methods=['GET'])
@jwt_required()
def getPosts():

    blog = db.getBlog()
    
    return jsonify(blog), 200

# getBlog devuelve todos los posts almacenados 

@app.route('/getDocuments', methods=['GET'])
@jwt_required()
def getDocuments():

    blog = db.getBlogFile()
    
    return jsonify(blog), 200


# getBlog devuelve todos los posts almacenados 

@app.route('/getVideos', methods=['GET'])
@jwt_required()
def getVideos():

    blog = db.getBlogVideo()
    
    return jsonify(blog), 200


# getImage devuelve imagenes almacenadas 

@app.route('/getBlogVideo/<name>', methods=['GET'])
#@jwt_required()
def getBlogVideo(name):

    file_path = os.path.join(app.config['UPLOAD_FOLDER_VIDEO'], f"{name}.mp4")
    range_header = request.headers.get('Range', None)

    if not range_header:
        # Si no se solicita un rango, devuelve el archivo completo
        return Response(open(file_path, 'rb'), mimetype='video/mp4')

    # Procesa el encabezado Range
    size = os.path.getsize(file_path)
    byte_start, byte_end = parse_range_header(range_header, size)

    with open(file_path, 'rb') as f:
        f.seek(byte_start)
        data = f.read(byte_end - byte_start + 1)
    
    response = Response(data, status=206, mimetype='video/mp4')
    response.headers['Content-Range'] = f"bytes {byte_start}-{byte_end}/{size}"
    response.headers['Accept-Ranges'] = 'bytes'
    response.headers['Content-Length'] = str(byte_end - byte_start + 1)

    return response

def parse_range_header(range_header, file_size):
    
    #Procesa el encabezado Range y devuelve los bytes inicio y fin.
    try:
        range_match = range_header.split("=")[1]
        byte_start, byte_end = range_match.split("-")
        byte_start = int(byte_start) if byte_start else 0
        byte_end = int(byte_end) if byte_end else file_size - 1
        return byte_start, min(byte_end, file_size - 1)
    except (ValueError, IndexError):
        abort(416, "Invalid Range")


# getImage devuelve imagenes almacenadas 

@app.route('/getBlogDocument/<name>', methods=['GET'])
#@jwt_required()
def getBlogDocument(name):

    file = name+'.pdf'
    print(file)
   
    return send_from_directory(app.config['UPLOAD_FOLDER_DOCUMENTS'], file, as_attachment=True ), 200

# getImage devuelve imagenes almacenadas 

@app.route('/getBlogImage/<name>', methods=['GET'])
@jwt_required()
def getBlogImage(name):

    file = name+'.jpg'
    print(file)
   
    return send_from_directory(app.config['UPLOAD_FOLDER_IMAGES'], file), 200

# newPost almacena un articulo en la base de datos

@app.route('/newPost', methods=['POST'])
@jwt_required()
def newPost():

    data = request.json

    titulo = data['title']
    articulo = data['message']

    db.addNewPost(titulo, articulo)
    
    return jsonify(), 200


@jwt_required()
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# newImage almacena un imagen en el servidor

@app.route('/newBlogVideo', methods=['POST'])
@jwt_required()
def newBlogVideo():
    data = request.json

    titulo = data['title']

    db.addNewVideo(titulo)
    
    return jsonify(), 200


# newImage almacena un imagen en el servidor

@app.route('/newBlogDocument', methods=['POST'])
@jwt_required()
def newBlogDocument():

    data = request.json
    titulo = data['title']
    db.addNewDocument(titulo)
    
    return jsonify(), 200



# newImage almacena un imagen en el servidor

@app.route('/newImage', methods=['GET', 'POST'])
@jwt_required()
def newImage():


    file = request.files['image']
    print(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], file.filename))


    return jsonify(), 200


# newImage almacena un imagen en el servidor

@app.route('/newVideo', methods=['GET', 'POST'])
@jwt_required()
def newVideo():

    file = request.files['video']
    print(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER_VIDEO'], file.filename))


    return jsonify(), 200


# newImage almacena un imagen en el servidor

@app.route('/newDocument', methods=['GET', 'POST'])
@jwt_required()
def newDocument():

    file = request.files['document']
    print(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER_DOCUMENTS'], file.filename))

    return jsonify(), 200



# modifyPost modifica un articulo en la base de datos

@app.route('/modifyPost', methods=['POST'])
@jwt_required()
def modifyPost():

    data = request.json

    titulo = data['title']
    tituloprev = data['oldtitle']
    articulo = data['message']

    db.modifyPost(titulo, tituloprev, articulo)
    os.rename(IMAGE_FOLDER+tituloprev+'.jpg', IMAGE_FOLDER+titulo+'.jpg')
    
    return jsonify(), 200

# modifyPost modifica un articulo en la base de datos

@app.route('/modifyBlogVideo', methods=['POST'])
@jwt_required()
def modifyBlogVideo():

    data = request.json

    titulo = data['title']
    tituloprev = data['oldtitle']
    articulo = data['message']

    db.modifyPost(titulo, tituloprev, articulo)
    os.rename(VIDEO_FOLDER+tituloprev+'.mp4', VIDEO_FOLDER+titulo+'.mp4')
    
    return jsonify(), 200

# modifyPost modifica un articulo en la base de datos

@app.route('/modifyBlogDocument', methods=['POST'])
@jwt_required()
def modifyBlogDocument():

    data = request.json

    titulo = data['title']
    tituloprev = data['oldtitle']
    articulo = data['message']

    db.modifyPost(titulo, tituloprev, articulo)
    os.rename(DOCUMENT_FOLDER+tituloprev+'.pdf', DOCUMENT_FOLDER+titulo+'.pdf')
    
    return jsonify(), 200


# modifyPost modifica un articulo en la base de datos

@app.route('/deletePost', methods=['POST'])
@jwt_required()
def deletePost():

    data = request.json

    titulo = data['title']
    db.deletePost(titulo)
    os.remove(IMAGE_FOLDER+titulo+'.jpg')
    
    return jsonify(), 200

# modifyPost modifica un articulo en la base de datos

@app.route('/deletePostVideo', methods=['POST'])
@jwt_required()
def deletePostVideo():

    data = request.json

    titulo = data['title']

    db.deletePost(titulo)
    os.remove(VIDEO_FOLDER+titulo+'.mp4')

    
    return jsonify(), 200

# modifyPost modifica un articulo en la base de datos

@app.route('/deletePostDocument', methods=['POST'])
@jwt_required()
def deletePostDocument():

    data = request.json

    titulo = data['title']

    db.deletePost(titulo)
    os.remove(DOCUMENT_FOLDER+titulo+'.pdf')

    
    return jsonify(), 200
    
   



##
## PETICIONES PARA OBTENER CHATS DE LA BASE DE DATOS
##


# Websocket chats

@socketio.on('connect', namespace='/chat')
def connect_chat():
    print('Connected chat')

@socketio.on('join', namespace='/chat')
def join_chat(alias):
    join_room(alias)

@socketio.on('leave', namespace='/chat')
def leave_chat(alias):
    leave_room(alias)

# Websocket message

@socketio.on('message', namespace='/chat')
def message_chat(data):
    
    alias = data[0]
    user = data[1]
    message = data[2]

    db.addNewMessage(alias, user, message)
    send(message=True, to=alias, broadcast=True, )

    

# getAllChats devuelve los usuarios con chats abiertos 

@app.route('/getAllChats', methods=['GET'])
@jwt_required()
def getAllChats():

    usuarios = db.getAllChats()
    
    return jsonify(usuarios), 200


# getStoredChat devuelve los usuarios con chats archivados

@app.route('/getPendingChats', methods=['GET'])
@jwt_required()
def getPendingChat():

    usuarios = db.getPendingChats()
    
    return jsonify(usuarios), 200


# getStoredChat devuelve los usuarios con chats archivados

@app.route('/getStoredChat', methods=['GET'])
@jwt_required()
def getStoredChat():

    usuarios = db.getStoredChats()
    
    return jsonify(usuarios), 200


# getAllChats devuelve los usuarios con chats abiertos 

@app.route('/setStoredChat', methods=['POST'])
@jwt_required()
def setStoredChat():
    
    data = request.json

    alias = data['alias']

    db.setStoredChat(alias)
    
    return jsonify(), 200


# getAllChats devuelve los usuarios con chats abiertos 

@app.route('/setPendingChat', methods=['POST'])
@jwt_required()
def setPendingChat():
    
    data = request.json

    alias = data['alias']

    db.setPendingChat(alias)
    
    return jsonify(), 200



# getChat devuelve el chat de un usuario concreto

@app.route('/getChat', methods=['POST'])
@jwt_required()
def getChat():

    data = request.json

    alias = data['alias']

    chat = db.getChat(alias)
    
    return jsonify(chat), 200



# sendMessage introduce la consulta de un usuario en la base de datos

@app.route('/sendMessage', methods=['POST'])
@jwt_required()
def sendMessage():

    data = request.json

    alias = data['alias']
    user = data['user']
    message = data['message']

    db.addNewMessage(alias, user, message)
    
    return jsonify(), 200


# getAllChats devuelve los usuarios con chats abiertos 

@app.route('/deleteChat', methods=['POST'])
@jwt_required()
def deleteChat():

    data = request.json

    alias = data['alias']
    
    db.deleteChat(alias)
    
    return jsonify(), 200



##
## PETICIONES PARA OBTENER SEMAFORO DE LA BASE DE DATOS
##

# getStoplight devuelve el codigo de color para el semaforo

@app.route('/getStoplight', methods=['GET'])
@jwt_required()
def getStoplight():

    stoplight = db.getStoplight()

    return jsonify(stoplight), 200


# setStoplight almacena el codigo de color para el semaforo

@app.route('/setStoplight', methods=['POST'])
@jwt_required()
def setStoplight():

    data = request.json

    neutral = data['neutral']
    ent_apx = data['ent_apx']
    ent_ent = data['ent_ent']
    sal_tp_apx= data['sal_tp_apx']
    sal_tp_sal = data['sal_tp_sal']
    sal_sl_apx = data['sal_sl_apx']
    sal_sl_sal = data['sal_sl_sal']
    
    db.modifyStoplight(neutral, ent_apx, ent_ent, sal_tp_apx, sal_tp_sal, sal_sl_apx, sal_sl_sal)

    return jsonify(), 200



# Ruta protegida // VER UNA VEZ QUE SE HA AUTENTICADO

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify(logged_in_as=current_user), 200




#python -m flask --app .\server.py run --host=0.0.0.0

#Para pruebas hay que permitir las conexiones remotas en red publica para Python en el Firewall de Windows