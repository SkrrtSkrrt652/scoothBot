import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://random-stuff-api.p.rapidapi.com/joke"
querystring = {"type": "any"}

headers = {
    "authorization": os.getenv("API_KEY"),
    "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
    "x-rapidapi-host": "random-stuff-api.p.rapidapi.com",
}


class CringeFinder:
    def cringe(self):
        flag = False
        while not flag:
            # fmt: off
            response = requests.request("GET", url, headers=headers,
                                        params=querystring)
            # fmt: on
            mssg_json = json.loads(response.text)
            flags = json.loads(json.dumps(mssg_json["flags"]))
            if (
                not flags["nsfw"]
                and not flags["religious"]
                and not flags["racist"]
                and not flags["sexist"]
            ):
                try:
                    msg = []
                    msg.append(mssg_json["setup"])
                    msg.append(mssg_json["delivery"])
                    return msg
                except Exception:
                    continue
