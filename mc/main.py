import json
import sys
import masscan
import asyncio
import random
from mcstatus import JavaServer
from db import *

""" READ CONFIG """
try:
    with open("/usr/app/config.json", 'r') as f:
        jConfig = json.loads(f.read())
except:
    print(f"[{TodayDate()}] [CRITICAL] Error failed on read config file!")
    sys.exit(0);

PORT = jConfig['MASSCAN'][0]['PORT']
RATE = jConfig['MASSCAN'][0]['RATE']
DBUSER = jConfig['APPLICATION'][0]['DB_USERNAME']
DBPASSWORD = jConfig['APPLICATION'][0]['DB_PASSWORD']
DBIP = jConfig['APPLICATION'][0]['DB_IP']
DBPORT = jConfig['APPLICATION'][0]['DB_PORT']

""" Import DB"""

DBMC = DBMongo(DBUSER, DBPASSWORD, DBIP, DBPORT)
conn_db = DBMC.connect_db()

""" Check if the Server or Player is already in Database <1day"""
def Exist1day(todayWorker, collection, content):
    GetAllData = DBMC.GetAllData(conn_db, collection) 
    
    if GetAllData == []:
        return False
    else:
        for Data in GetAllData:
            todaySplited = Data['date'].split('/')
            todayWorkerSplited = todayWorker.split('/')
            if collection == "server":
                if content == Data['ip'] and todayWorkerSplited[0] == todaySplited[0]:
                    return True
                else:
                    return False
            elif collection == "player":
                if content == Data['uuid'] and todayWorkerSplited[0] == todaySplited[0]:
                    return True
                else:
                    return False

""" Check if is a minecraft server and get info """

async def mcStatus(IP, PORT):
    print(f"[{TodayDate()}] [INFO] Checking IP: {IP}:{PORT}")
    try:
        server = JavaServer.lookup(f"{IP}:{PORT}")
        status = server.status()
        if(Exist1day(TodayDate(), 'server', IP) == False):
            DBMC.DeleteDataFromServer(conn_db, IP)
            server_info = Server(IP, PORT, status.description, status.version.name, status.players.online, status.players.max, status.favicon, status.raw, TodayDate())
            DBMC.InsertServer(conn_db, server_info)
            print(f"[{TodayDate()}] [INFO] Minecraft Server Found! IP: {IP}:{PORT}")
        
            if status.players.sample != None:
                for player in status.players.sample:
                    if(Exist1day(TodayDate(), 'player', player.id) == False):
                        DBMC.DeleteDataFromPlayer(conn_db, player.id)
                        player_info = Player(player.name, player.id, IP, PORT)
                        DBMC.InsertPlayer(conn_db, player_info, TodayDate())
                    else:
                        print(f"[{TodayDate()}] [INFO] The Player already in Database (<1 Day)")
        else:
            print(f"[{TodayDate()}] [INFO] The Server already in Database (<1 Day)")
    except Exception as e:
        print(f"[{TodayDate()}] [CRITICAL] MC STATUS:", e)
        

if __name__ == "__main__":
    print(f"[{TodayDate()}] [INFO] Generating IP RANGES...")
    ESP1 = list(range(1,255))
    ESP2 = list(range(1,255))
    random.shuffle(ESP1)
    random.shuffle(ESP2)
    ip_ranges = []
    for A in ESP1:
        for B in ESP2:
            ip_range = f"{A}.{B}.0.0/16"
            ip_ranges.append(ip_range)
    print(f"[{TodayDate()}] [INFO] Generating IP RANGES Over!")
    while True:
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        random.shuffle(ip_ranges)
        for IP_RANGE in ip_ranges:
            print(f"[{TodayDate()}] [INFO] Starting Scan: {IP_RANGE}")
            try:
                mas = masscan.PortScanner()
                mas.scan(IP_RANGE, ports=PORT, arguments=f'--rate {RATE} --exclude 255.255.255.255')
                jScanResult = json.loads(mas.scan_result)
                for IP in jScanResult["scan"]:
                    #mcStatus(IP, jScanResult["scan"][IP][0]['port'])
                        loop.run_until_complete(mcStatus(IP, jScanResult["scan"][IP][0]['port']))
                
            except masscan.NetworkConnectionError:
                print(f"[{TodayDate()}] [CRITICAL] masscan masscan.masscan.NetworkConnectionError")
            
            
            print(f"[{TodayDate()}] [INFO] Scan on {IP_RANGE} is Over!")
        loop.close()
        

    

