import urllib3
import json
import math
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

def DetermineCardinalPoint(strToAnalyze):
    switcher = {
        "N": "Nord",
        "E": "Est",
        "S": "Sud",
        "W": "Ouest"
    }

    return switcher.get(strToAnalyze, "Ce point cardinal n'existe pas !");

def checkIfTrameIsSupported(strToAnalyze):
    switcher = {
        "$GPGGA": "true"
    }

    return switcher.get(strToAnalyze, "Cette trame n'est pas supporté pour le moment !")

fichier = "code1.txt"

L = 128

with open(fichier, 'r') as fich:
    for i in range(L):
        ligne = fich.readline()
    champs = ligne.split(",")
    if checkIfTrameIsSupported(champs[0]) == "true":
        print("Trame envoyée à", champs[1][0: 2], "heures", champs[1][2: 4], "minutes et", champs[1][4: 6], "secondes")
        print("Latitude : ", float(champs[2]) / 100, " degrés ", DetermineCardinalPoint(champs[3]), sep="")
        print("Longitude : ", float(champs[4]) / 100, " degrés ", DetermineCardinalPoint(champs[5]), sep="")
        print("Nombre de satellite(s) utilisé(s) afin de faire les calculs :", champs[7].replace("0", "", 1) if champs[7][0: 1] == "0" else champs[7])
        pool_manager = urllib3.PoolManager()
        list = [float(champs[2]) / 100, float(champs[4]) / 100]
        longitudeAndLatitude = ','.join(map(str, list))
        response = pool_manager.request("GET", "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey={}&mode=retrieveAddresses&prox={}".format(config.get('HEREAPI', 'APIKEY'), longitudeAndLatitude))
        cityName = json.loads(response.data.decode('utf8'))
        print("Ville :", cityName["Response"]["View"][0]["Result"][0]["Location"]["Address"]["City"])
        input('Press any key to exit')
