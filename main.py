import discord
import requests
import json
import time
import search
client = discord.Client()

url = "https://random-stuff-api.p.rapidapi.com/joke/any"

querystring = {"api_key":"TctfASVGKw6P"}

headers = {
    'x-api-key': "TctfASVGKw6P",
    'x-rapidapi-key': "8d718b9663msh96c9ff6652097dbp1d7662jsn93807b8c1a1c",
    'x-rapidapi-host': "random-stuff-api.p.rapidapi.com"
    }


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

mssg_json = json.loads("{}")

@client.event
async def on_message(message):

    categories = ['artliterature', 'language', 'sciencenature', 'general', 'fooddrinkn', 'peopleplaces', 'geography', 'historyholidays', 'entertainment', 'toysgames', 'music mathematics', 'religionmythology', 'sportsleisure']

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$Changes'):
        await message.channel.send('Nothing useful')
    elif message.content.startswith('$random'):
        flag = False
        while not flag:
            response = requests.request("GET", url, headers=headers, params=querystring)
            mssg_json = json.loads(response.text)
            flags = json.loads(json.dumps(mssg_json["flags"]))
            if not flags["nsfw"] and not flags["religious"] and not flags["racist"] and not flags["sexist"]:
                await message.channel.send(mssg_json["setup"])
                time.sleep(2)
                await message.channel.send(mssg_json["delivery"])
                flag = True
    elif message.content.startswith("$help questions"):
        await message.channel.send("format : $question <CATEGORY> <NUMBER OF QUESTIONS>\n Example : $question sciencenature 3")
        await message.channel.send("Available Categories :")
        list = ""
        for category in categories:
            list += "       "+category + "\n"
        await message.channel.send(list)
    elif message.content.startswith("$question"):
        input = message.content.split()
        if len(input) == 3 and categories.count(input[1]) and input[2].isnumeric():
            get_questions = search.question()
            for i in range(int(input[2])):
                question = get_questions.get_questions(input[1])
                await message.channel.send(question['question'])
                if
client.run('ODU3NTU2ODAwMDAxNTQwMTE3.YNRUAQ.4ikv-ocvTyn5st4il6ftZb_j2a8')