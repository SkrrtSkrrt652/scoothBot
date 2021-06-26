import requests
import discord
import json
import time

url = "https://random-stuff-api.p.rapidapi.com/joke/any"

querystring = {"api_key": "TctfASVGKw6P"}

headers = {
    'x-api-key': "TctfASVGKw6P",
    'x-rapidapi-key': "8d718b9663msh96c9ff6652097dbp1d7662jsn93807b8c1a1c",
    'x-rapidapi-host': "random-stuff-api.p.rapidapi.com"
}

class CringeFinder:
    def cringe(self):
        flag = False
        while not flag:
            response = requests.request("GET", url, headers=headers, params=querystring)
            mssg_json = json.loads(response.text)
            flags = json.loads(json.dumps(mssg_json["flags"]))
            if not flags["nsfw"] and not flags["religious"] and not flags["racist"] and not flags["sexist"]:
                try:
                    msg= []
                    msg.append(mssg_json["setup"])
                    msg.append(mssg_json["delivery"])
                    return msg
                except:
                    continue
