import json

import discord
import quick_search
from discord.ext import commands

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def search(ctx, query,number):
    search = quick_search.QuickSearch()
    await ctx.send("**" +query.upper()+ "**")
    raw_img_data = search.quickImageSearch(query=query.lower(),number=number)
    for i in range(int(number)):
        try:
            img_data = json.loads(json.dumps(raw_img_data[i]))
            img_data = json.loads(json.dumps(img_data["thumbnail"]))
            await ctx.send(img_data["thumbnailUrl"])
        except:
            continue
    links= "__**"
    await ctx.send("_**WAIT I AM NOT DONE YET, I'M A LITTLE SLOW**_")
    raw_data = search.quickSearch(query=query,number=number)
    for i in range(int(number)):
        try:
            data = json.loads(json.dumps(raw_data[i]))
            links += data["link"] +" \n"
        except:
            continue
    links += "**__"
    await ctx.send("** Links for more reference **:")
    await ctx.send(links)


@bot.command()
async def display(ctx):
    await ctx.send(
        'https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixid'
        '=MnwxMjA3fDB8MHxzZWFyY2h8NHx8cGljfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&w=1000&q=80')

bot.run('<AUTHORIZATION>')
