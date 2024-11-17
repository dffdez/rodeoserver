import psycopg2


IP_DATABASE = 'rodeo_database'
PORT_DATABASE = '5432'



#This function adds quotation marks to parameters
def qmarks(cadena):
    cadenaMarks = "'"+cadena+"'"
    return cadenaMarks



#
# USERS LOGIN AND SIGNUP
#

# login returns if an user is registered

def login (alias, contrasenia):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    try:

        cursor = conn.cursor()

        cursor.execute("SELECT Alias, Contrasenia, Admin from USUARIOS WHERE Alias="+qmarks(alias)+" AND Contrasenia="+qmarks(contrasenia)+";")
        credentials = cursor.fetchone()
        conn.close()
        return credentials

    except:
        conn.close()
        return False






# addNewUser insert a new user into USUARIOS table

def addNewUser (alias, contrasenia, nombre, apellido, email):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )


    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO USUARIOS (Alias, Contrasenia, Nombre, Apellido, Email) VALUES ("+
                    qmarks(alias)+", "+qmarks(contrasenia)+", "+qmarks(nombre)+", "+qmarks(apellido)+", "+qmarks(email) +");")

        conn.commit()   # Hace efectivos los cambios para todas las sesiones  
        conn.close()
        return True

    except:
        conn.close()
        return False

    # addNewUser insert a new user into USUARIOS table

def addNewAdmin (alias, contrasenia, nombre, apellido, email):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )


    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO USUARIOS (Alias, Contrasenia, Nombre, Apellido, Email, Admin) VALUES ("+
                    qmarks(alias)+", "+qmarks(contrasenia)+", "+qmarks(nombre)+", "+qmarks(apellido)+", "+qmarks(email) +", "+qmarks(str(1))+");")

        conn.commit()   # Hace efectivos los cambios para todas las sesiones  
        conn.close()
        return True

    except:
        conn.close()
        return False


# deleteUser delete a user profile from USUARIOS table
    
def deleteUser (alias):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM USUARIOS WHERE Alias="+qmarks(alias)+";")
    cursor.execute("DELETE FROM FAVORITOS WHERE Alias="+qmarks(alias)+";")
    cursor.execute("DELETE FROM CHAT WHERE Alias="+qmarks(alias)+";")

    conn.commit()
    conn.close()


#getAllUser return all users alias

def getAllUser():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("SELECT Alias FROM USUARIOS;")
    usersalias = cursor.fetchall()
    conn.close()

    return usersalias



#getUser returns all information of an user

def getUser(alias):
    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("SELECT Alias, Contrasenia, Nombre, Apellido, Email FROM USUARIOS WHERE Alias="+qmarks(alias)+";")
    userinfo = cursor.fetchone()
    conn.close()

    return userinfo



#modifyUser allows to change a user's password

def modifyUserPass(alias, contrasenia):
    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE USUARIOS SET Contrasenia="+qmarks(contrasenia)+"WHERE Alias="+qmarks(alias)+";")
    conn.commit()
    conn.close()



#modifyUser allows to change a user's password

def modifyUserData(alias, nombre, apellido, email):
    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE USUARIOS SET Nombre="+qmarks(nombre)+", Apellido="+qmarks(apellido)+", Email="+qmarks(email)+"WHERE Alias="+qmarks(alias)+";")
    conn.commit()
    conn.close()



# tokenPushNotification store a token for push notifications in database

def setPushNotificationToken(alias, token):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE USUARIOS SET NotificationToken="+qmarks(token)+"WHERE Alias="+qmarks(alias)+";")
    conn.commit()
    conn.close()


# tokenPushNotification store a token for push notifications in database

def getPushNotificationToken():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("SELECT Alias, NotificationToken FROM USUARIOS;")
    
    tokens = cursor.fetchall()

    conn.close()

    return tokens



# tokenJWT store a token for authentication in database

def setTokenJWT(alias, token):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE USUARIOS SET Nombre="+qmarks(nombre)+", Apellido="+qmarks(apellido)+", Email="+qmarks(email)+"WHERE Alias="+qmarks(alias)+";")
    conn.commit()
    conn.close()


# tokenJWT get a token for authentication from database

def getTokenJWT(alias, token):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE USUARIOS SET Nombre="+qmarks(nombre)+", Apellido="+qmarks(apellido)+", Email="+qmarks(email)+"WHERE Alias="+qmarks(alias)+";")
    conn.commit()
    conn.close()




#
# STOCKS
#


# getStocks returns all stocks from VALORES table

def getStocks ():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * from VALORES;") 
    stocks = cursor.fetchall()

    conn.close()

    return stocks

# getStocksName returns all stocks names from VALORES table

def getStocksName ():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("SELECT Simbolo, Estado, AC, ValorEntrada, TiempoSalida from VALORES;") 
    stocksname = cursor.fetchall()

    conn.close()

    return stocksname



# getFavourites returns all stocks from FAVORITOS table

def getFavourites (alias):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * from VALORES WHERE Simbolo IN (SELECT Simbolo from FAVORITOS WHERE Alias="+qmarks(alias)+");") 
    stocks = cursor.fetchall()

    conn.close()

    return stocks



# getTokenByFavourite returns push notification token from VALORES table giving a stock

def getTokenByFavourite (stock):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("SELECT NotificationToken from USUARIOS WHERE Alias IN (SELECT Alias from FAVORITOS WHERE Simbolo="+qmarks(stock)+");") 
    stocks = cursor.fetchall()

    conn.close()

    return stocks



# setFavourite returns all stocks from VALORES table

def setFavourite (alias, simbolo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("INSERT INTO FAVORITOS (Simbolo, Alias) VALUES ("+qmarks(simbolo)+", "+qmarks(alias)+");") 
    conn.commit()

    conn.close()



# deleteFavourite returns all stocks from VALORES table

def deleteFavourite (alias, simbolo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM FAVORITOS WHERE Simbolo="+qmarks(simbolo)+"AND Alias="+qmarks(alias)+";")
    conn.commit()

    conn.close()





#addNewStock adds a new stock to VALORES table

def addNewStock (simbolo, nombre, ac):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    

    cursor = conn.cursor()
    cursor.execute("INSERT INTO VALORES (Simbolo, Nombre, AC) VALUES ("+
                qmarks(simbolo)+", "+qmarks(nombre)+", "+qmarks(ac)+");")
    cursor.execute("INSERT INTO LIMITES (Simbolo) VALUES ("+ qmarks(simbolo)+");")
    
    conn.commit()
    
    conn.close()




#deleteStock deletes a stock from VALORES table

def deleteStock (simbolo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM VALORES WHERE Simbolo="+qmarks(simbolo)+";")
    cursor.execute("DELETE FROM LIMITES WHERE Simbolo="+qmarks(simbolo)+";")
    cursor.execute("DELETE FROM FAVORITOS WHERE Simbolo="+qmarks(simbolo)+";")


    conn.commit()
    conn.close()


# modifyStock change the state of an stock

def modifyStock(simbolo, estado):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE VALORES SET Estado="+qmarks(str(estado))+"' WHERE Simbolo="+qmarks(simbolo)+";")
    conn.commit()
    conn.close()



#
# LIMITS
#



#getLimits gets limits of a stock
    
def getLimits(simbolo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LIMITES WHERE Simbolo="+qmarks(simbolo)+";")
    limits = cursor.fetchone()
    conn.close()

    return limits


#deleteLimits deletes limits of a stock
    
def deleteLimits(simbolo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM LIMITES WHERE Simbolo="+qmarks(simbolo)+";")
    conn.commit()
    conn.close()



#modifyLimits modifies limits of a stock
    
def setLimits(simbolo, e_apx_rsi_min, e_apx_rsi_max, e_apx_stoch_min, e_apx_stoch_max, e_ent_rsi_min, e_ent_rsi_max, e_ent_stoch_min,
	e_ent_stoch_max, stp_apx_stoch_min, stp_apx_stoch_max, stp_sal_stoch_min, ssl_apx_value_min, ssl_apx_value_max, ssl_sal_value_min):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE LIMITES SET e_apx_rsi_min="+qmarks(str(e_apx_rsi_min))+", e_apx_rsi_max="+qmarks(str(e_apx_rsi_max))+", e_apx_stoch_min="+qmarks(str(e_apx_stoch_min))+
                   ", e_apx_stoch_max="+qmarks(str(e_apx_stoch_max))+", e_ent_rsi_min="+qmarks(str(e_ent_rsi_min))+", e_ent_rsi_max="+qmarks(str(e_ent_rsi_max))+", e_ent_stoch_min="+qmarks(str(e_ent_stoch_min))+","+
                   "e_ent_stoch_max="+qmarks(str(e_ent_stoch_max))+", stp_apx_stoch_min="+qmarks(str(stp_apx_stoch_min))+", stp_apx_stoch_max="+qmarks(str(stp_apx_stoch_max))+", stp_sal_stoch_min="+qmarks(str(stp_sal_stoch_min))+
                   ", ssl_apx_value_min="+qmarks(str(ssl_apx_value_min))+", ssl_apx_value_max="+qmarks(str(ssl_apx_value_max))+", ssl_sal_value_min="+qmarks(str(ssl_sal_value_min))+" WHERE Simbolo="+qmarks(simbolo)+";")
    conn.commit()
    conn.close()



#getLimits gets limits of a stock
    
def getLimitsRef(simbolo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LIMITESREF WHERE Simbolo="+qmarks(simbolo)+";")
    limits = cursor.fetchone()
    conn.close()

    return limits



#modifyLimits modifies limits of a stock
    
def setLimitsRef(simbolo, e_apx_rsi_min, e_apx_rsi_max, e_apx_stoch_min, e_apx_stoch_max, e_ent_rsi_min, e_ent_rsi_max, e_ent_stoch_min,
	e_ent_stoch_max, stp_apx_stoch_min, stp_apx_stoch_max, stp_sal_stoch_min, ssl_apx_value_min, ssl_apx_value_max, ssl_sal_value_min):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE LIMITESREF SET e_apx_rsi_min="+qmarks(str(e_apx_rsi_min))+", e_apx_rsi_max="+qmarks(str(e_apx_rsi_max))+", e_apx_stoch_min="+qmarks(str(e_apx_stoch_min))+
                   ", e_apx_stoch_max="+qmarks(str(e_apx_stoch_max))+", e_ent_rsi_min="+qmarks(str(e_ent_rsi_min))+", e_ent_rsi_max="+qmarks(str(e_ent_rsi_max))+", e_ent_stoch_min="+qmarks(str(e_ent_stoch_min))+","+
                   "e_ent_stoch_max="+qmarks(str(e_ent_stoch_max))+", stp_apx_stoch_min="+qmarks(str(stp_apx_stoch_min))+", stp_apx_stoch_max="+qmarks(str(stp_apx_stoch_max))+", stp_sal_stoch_min="+qmarks(str(stp_sal_stoch_min))+
                   ", ssl_apx_value_min="+qmarks(str(ssl_apx_value_min))+", ssl_apx_value_max="+qmarks(str(ssl_apx_value_max))+", ssl_sal_value_min="+qmarks(str(ssl_sal_value_min))+" WHERE Simbolo="+qmarks(simbolo)+";")
    conn.commit()
    conn.close()



#setState modifies state of a stock
    
def setState(simbolo, estado):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE VALORES SET Estado="+qmarks(str(estado))+" WHERE Simbolo="+qmarks(simbolo)+";")
    conn.commit()
    conn.close()


    #setState modifies state of a stock
    
def setValorEntrada(simbolo, valor):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE VALORES SET ValorEntrada="+qmarks(str(valor))+" WHERE Simbolo="+qmarks(simbolo)+";")
    conn.commit()
    conn.close()



#setState modifies state of a stock
    
def setTiempoSalida(simbolo, tiempo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE VALORES SET TiempoSalida="+qmarks(str(tiempo))+" WHERE Simbolo="+qmarks(simbolo)+";")
    conn.commit()
    conn.close()




#
# BLOG
#

# getBlog returns all from BLOG table

def getBlog():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor() 
    cursor.execute("SELECT Titulo, Articulo FROM BLOG WHERE Tipo='post' order by Fecha;")
    blog = cursor.fetchall()
    conn.close()

    return blog

# getBlog returns all from BLOG table

def getBlogFile():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor() 
    cursor.execute("SELECT Titulo, Articulo FROM BLOG WHERE Tipo='file' order by Fecha;")
    blog = cursor.fetchall()
    conn.close()

    return blog


# getBlog returns all from BLOG table

def getBlogVideo():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor() 
    cursor.execute("SELECT Titulo, Articulo FROM BLOG WHERE Tipo='video' order by Fecha;")
    blog = cursor.fetchall()
    conn.close()

    return blog




# addNewPost adds a new entry into BLOG table

def addNewPost(titulo, articulo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor() 

    cursor.execute("INSERT INTO BLOG (Titulo, Articulo, Fecha) VALUES ("+qmarks(titulo)+", "+qmarks(articulo)+" , current_timestamp);")
    conn.commit()
    conn.close()


# addNewDocument adds a new entry into BLOG table

def addNewDocument(titulo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor() 

    cursor.execute("INSERT INTO BLOG (Titulo, Fecha, Tipo) VALUES ("+qmarks(titulo)+", current_timestamp, 'file');")
    conn.commit()
    conn.close()


# addNewVideo adds a new entry into BLOG table

def addNewVideo(titulo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor() 

    cursor.execute("INSERT INTO BLOG (Titulo, Fecha, Tipo) VALUES ("+qmarks(titulo)+", current_timestamp, 'video');")
    conn.commit()
    conn.close()



# deletePost deletes a Post from BLOG table by ID

def deletePost(titulo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM BLOG WHERE Titulo="+ qmarks(titulo)+";")
    conn.commit()
    conn.close()



# modifyPost modifies a entry from BLOG table

def modifyPost(titulo, tituloprev, articulo):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE BLOG SET Titulo="+qmarks(titulo)+", Articulo="+qmarks(articulo)+" WHERE Titulo="+qmarks(tituloprev)+";")
    conn.commit()
    conn.close()





#
# CHAT
#


# addMessage adds a new entry into CHAT table

def addNewMessage(alias, usuario, mensaje):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    #Hay que añadir fecha para ordenar mensajes

    cursor.execute("INSERT INTO CHAT (Alias, Usuario, Mensaje, Fecha) VALUES ("+qmarks(alias)+", "+qmarks(usuario)+", "+qmarks(mensaje)+", current_timestamp);")
    conn.commit()
    conn.close()



# getAllChats return name of users with chats

def getAllChats():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT Alias FROM CHAT WHERE Usuario='0';")
    usersChat = cursor.fetchall()
    conn.close()

    return usersChat



# getAllChats return name of users with chats

def getPendingChats():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT Alias FROM CHAT WHERE Usuario='0' AND Estado='0';")
    usersChat = cursor.fetchall()
    conn.close()

    return usersChat


# getStoredChats return name of users with chats stored

def getStoredChats():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT Alias FROM CHAT WHERE Usuario='0' AND Estado='1';")
    usersChat = cursor.fetchall()
    conn.close()

    return usersChat


# setStoredChat changes chat state to stored

def setStoredChat(alias):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("UPDATE CHAT SET Estado='1' WHERE Alias="+qmarks(alias)+";")
    conn.commit()

    conn.close()


# setPendingChat changes chat state to stored

def setPendingChat(alias):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("UPDATE CHAT SET Estado='0' WHERE Alias="+qmarks(alias)+";")
    conn.commit()

    conn.close()



# getChat returns a user's chat

def getChat(alias):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("SELECT Usuario, Mensaje FROM CHAT WHERE Alias="+qmarks(alias)+" order by Fecha;")
    usersChat = cursor.fetchall()
    conn.close()

    return usersChat


# deleteUser delete a user profile from USUARIOS table
    
def deleteChat (alias):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("DELETE FROM CHAT WHERE Alias="+qmarks(alias)+";")
    conn.commit()
    conn.close()


#
# STOPLIGHT
#

# getStoplight returns all from SEMAFORO table

def getStoplight():

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM SEMAFORO;")
    stoplight = cursor.fetchone()
    conn.close()

    return stoplight


# modifyPost modifies a entry from BLOG table

def modifyStoplight(neutral, ent_apx, ent_ent, sal_tp_apx, sal_tp_sal, sal_sl_apx, sal_sl_sal):

    conn = psycopg2.connect(
    database = "rodeo",
    host = IP_DATABASE,
    user="rodeo",
    password="votned-1ryCro",
    port=PORT_DATABASE
    )

    cursor = conn.cursor()
    cursor.execute("UPDATE SEMAFORO SET neutral="+qmarks(neutral)+", ent_apx="+qmarks(ent_apx)+", ent_ent="+qmarks(ent_ent)
                   +", sal_tp_apx="+qmarks(sal_tp_apx)+", sal_tp_sal="+qmarks(sal_tp_sal)+", sal_sl_apx="+qmarks(sal_sl_apx)
                   +", sal_sl_sal="+qmarks(sal_sl_sal)+";")
    conn.commit()
    conn.close()

