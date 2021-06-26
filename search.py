import json

import requests
import  re

url = "https://trivia-by-api-ninjas.p.rapidapi.com/v1/trivia"


headers = {
    'x-rapidapi-key': "8d718b9663msh96c9ff6652097dbp1d7662jsn93807b8c1a1c",
    'x-rapidapi-host': "trivia-by-api-ninjas.p.rapidapi.com"
    }
class question:

    def get_questions(self,category,limit = "1"):
        querystring = {"category": category, "limit": "1"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
        data = json.loads(json.dumps(data[0]))
        return data