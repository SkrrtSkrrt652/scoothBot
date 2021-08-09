import json

import requests


class QuickSearch:
    def quickImageSearch(self, query="iron man", number=1):
        querystring = {"q": query}

        headers = {
            "x-rapidapi-key": "KEY",
            "x-rapidapi-host": "bing-image-search1.p.rapidapi.com",
        }

        img_url = "https://bing-image-search1.p.rapidapi.com/images/search"
        img_response_raw = requests.request(
            "GET", img_url, headers=headers, params=querystring
        )
        img_response = json.loads(img_response_raw.text)
        print(img_response)
        img_response = json.loads(json.dumps(img_response["relatedSearches"]))
        # img_response = json.loads(json.dumps(img_response[0]))
        # img_response = json.loads(json.dumps(img_response["image"]))
        # print(json.dumps(img_response))
        return img_response

    def quickSearch(self, query, number=1):
        query = query.strip()
        query = query.replace(" ", "+")

        url = (
            "https://google-search3.p.rapidapi.com/api/v1/search/q="
            + query
            + "&num="
            + str(number)
        )

        headers = {
            "x-rapidapi-key": "KEY",
            "x-rapidapi-host": "google-search3.p.rapidapi.com",
        }

        response = requests.request("GET", url, headers=headers)
        data_json = json.loads(response.text)
        data_json = json.loads(json.dumps(data_json["results"]))

        return data_json
