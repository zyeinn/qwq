import pymongo
from datetime import datetime


""" Get Today Date and Time"""
def TodayDate():
    now = datetime.now()
    today = now.strftime("%d/%m/%Y %H:%M:%S")
    return today

       

class Server:
    def __init__(self, ip, port, motd, version, online_players, max_players, favicon, raw, date_time):
        self.ip = ip
        self.port = port
        self.motd = motd,
        self.version = version,
        self.online_players = online_players,
        self.max_players = max_players,
        self.favicon = favicon,
        self.raw = raw,
        self.date_time = date_time

class Player:
    def __init__(self, name, uuid, server, port):
        self.name = name
        self.uuid = uuid
        self.server = server
        self.port = port

class DBMongo:
    def __init__(self, DBUSER, DBPASSWORD, DBIP, DBPORT):
        self.DBUSER = DBUSER
        self.DBPASSWORD = DBPASSWORD
        self.DBIP = DBIP
        self.DBPORT = DBPORT

    """ Connection to Mongo DB """
    def connect_db(self):
        try:
            client = pymongo.MongoClient(f"mongodb://{self.DBUSER}:{self.DBPASSWORD}@{self.DBIP}:{self.DBPORT}/?authSource=admin")
            db = client['qwq_minecraft']

        except Exception as e:
            print("Error on Connect DB: ", e)
        return db
       
    def InsertServer(self, db, server):
        server_info = {
            "ip": server.ip,
            "port": server.port,
            "motd": server.motd[0],
            "version": server.version[0],
            "online_players": server.online_players[0],
            "max_players": server.max_players[0],
            "favicon": str(server.favicon),
            "raw": str(server.raw),
            "date": str(server.date_time)
        }
        db_collec = db['server']
        try:
            db_collec.insert_one(server_info)
            print(f"[{TodayDate()}] [INFO] Server {server.ip} inserted!")
        except Exception as e:
            print(f"[{TodayDate()}] [CRITICAL] DB Exception on Insert Server Info: ", e)

    def InsertPlayer(self, db, player, date_time):
        db_collec = db['player']

        player_info = {
            "name": player.name,
            "uuid": player.uuid,
            "ip": player.server,
            "port": player.port,
            "date": str(date_time)
        }
        try:
            db_collec.insert_one(player_info)
            print(f"[{TodayDate()}] [INFO] Player {player.name} inserted!")
        except Exception as e:
            print(f"[{TodayDate()}] [CRITICAL] DB Exception on Insert Player Info: ", e)
    
    def GetAllData(self, db, collection):
        """ Get all Data Fro Collection """
        try:
            db_collec = db[collection]
            return list(db_collec.find({}))
        except Exception as e:
            print(f"[{TodayDate()}] [CRITICAL] DB Exception on Get all Data From Collection: ", e)

    def DeleteDataFromServer(self, db, server_ip):
        """ Delete Document From Server Collection """
        
        query = { 
            "ip": server_ip 
            }

        try:
            db_collec = db['server']
            db_collec.delete_one(query)
        except Exception as e:
            print(f"[{TodayDate()}] [CRITICAL] DB Exception on Delete Document Server From Collection: ", e)
    
    def DeleteDataFromPlayer(self, db, player_uuid):
        """ Delete Document From Player Collection """
        
        query = { 
            "uuid": player_uuid 
            }
        try:
            db_collec = db['player']
            db_collec.delete_one(query)
        except Exception as e:
            print(f"[{TodayDate()}] [CRITICAL] DB Exception on Delete Document Player From Collection: ", e)
