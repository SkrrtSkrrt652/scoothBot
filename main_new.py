import discord
import requests
import json
import time

from discord.ext.commands import Bot
from discord.ext import commands

import search

url = "https://random-stuff-api.p.rapidapi.com/joke/any"

querystring = {"api_key": "TctfASVGKw6P"}

headers = {
    'x-api-key': "TctfASVGKw6P",
    'x-rapidapi-key': "8d718b9663msh96c9ff6652097dbp1d7662jsn93807b8c1a1c",
    'x-rapidapi-host': "random-stuff-api.p.rapidapi.com"
}

bot = Bot(command_prefix='$')


@bot.command()
async def _help(ctx):
    categories = ['artliterature', 'language', 'sciencenature', 'general', 'fooddrinkn', 'peopleplaces', 'geography',
                  'historyholidays', 'entertainment', 'toysgames', 'music mathematics', 'religionmythology',
                  'sportsleisure']
    await ctx.send("format : $question <CATEGORY> <NUMBER OF QUESTIONS>\n Example : $question sciencenature 3")
    await ctx.send("Available Categories :")
    list = ""
    for category in categories:
        list += "\t\t" + category + "\n"
    await ctx.send(list)


@bot.command
async def question(ctx, question, limit):
    if limit.isnumeric() and int(limit) == 3 and categories.count(question):
        get_questions = search.question()
        for i in range(int(limit)):
            q = get_questions.get_questions(input[1])
            await ctx.send(question['question'])
            # if


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


mssg_json = json.loads("{}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
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


# bot.add_command(_help)
# bot.add_command(question)
bot.run('ODU3NTU2ODAwMDAxNTQwMTE3.YNRUAQ.aeKs7Dsy5n1w_Ldc4W26mDR3T7A')
