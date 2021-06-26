import discord
import requests
import json
import time
import cringe
from discord.ext.commands import Bot
from discord.ext import commands

import search

bot = Bot(command_prefix='$')

categories = ['artliterature', 'language', 'sciencenature', 'general', 'fooddrinkn', 'peopleplaces', 'geography',
                  'historyholidays', 'entertainment', 'toysgames', 'music mathematics', 'religionmythology',
                  'sportsleisure']

@bot.command()
async def _help(ctx):
    await ctx.send("format : $question <CATEGORY> <NUMBER OF QUESTIONS>\n Example : $question sciencenature 3")
    await ctx.send("Available Categories :")
    list = ""
    global categories
    for category in categories:
        list += "\t\t" + category + "\n"
    await ctx.send(list)


@bot.command()
async def question(ctx, question, limit):
    global categories
    # try:
    if limit.isnumeric() and categories.count(question):
        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author
        get_question = search.question()
        for i in range(int(limit)):
            q = get_question.get_questions(category=str(question))
            if not q == None:
                await ctx.send(q['question'])
                msg = await bot.wait_for("message",check=check)
                msg_list = []
                try:
                    msg_list.append(q["answer"].split().lower())
                except:
                    msg_list.append(q['answer'].lower)
                print(msg_list)
                if str(q['answer']).lower() == str(msg.content).lower() or msg_list.count(msg.content.lower):
                    await ctx.send("Woohoo! Thats the right ans! 😄") if str(q['answer']).lower() == str(msg.content).lower() else await ctx.send("Thats right, but the complete ans is : "+ q['answer'] +" 😄")
                else:
                    await ctx.send("The answer is "+ q["answer"]+" 🥺")
    elif categories.count(question):
        await ctx.send("Category not available, heres some help")
        await _help(ctx)
    else:
        await ctx.send("Dammit dude stick to them rules")
    # except:
    #     await ctx.send("Incorrect usage enter '$_help' for help \nCorrect usage : $question <CATEGORY> <NUMBER OF QUESTIONS>...")
Cyringe = cringe.CringeFinder
@bot.command()
async def cringe(ctx):
    msg = Cyringe.cringe(ctx)
    await ctx.send(msg[0])
    time.sleep(2)
    await ctx.send(msg[1])

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run('ODU3NTU2ODAwMDAxNTQwMTE3.YNRUAQ.1A58a0mRmijPsB5r16My08hgg5A')
