from inspect import Attribute
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import time
import requests
import json

import Classroom
import cringe
import search

intents = discord.Intents.all()
bot = Bot(command_prefix='$', intents=intents)

attendance = Classroom.Attendance() 

categories = ['artliterature', 'language', 'sciencenature', 'general', 'fooddrinkn', 'peopleplaces', 'geography',
                  'historyholidays', 'entertainment', 'toysgames', 'music mathematics', 'religionmythology',
                  'sportsleisure']

def prettier_time(time):
    time = int(time)
    if time < 60:
        return f'{time}s\n'
    elif time // 60 < 60:
        return f'{time//60}m {time % 60}s\n'
    else:
        return f'{time//3600}h {(time % 3600) // 60}m\n'




@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Track changes in the class voice channel if attendance is being tracked
@bot.event
async def on_voice_state_update(member, before, after):
    if attendance.track_voice_attendance:
        if before.channel != after.channel:
            if after.channel == attendance.classroom_vc:
                if member in attendance.vc_attendance:
                    attendance.vc_attendance[member][1] = time.time()
                else:
                    attendance.vc_attendance[member] = [0, time.time()]
            if before.channel == attendance.classroom_vc:
                    attendance.vc_attendance[member][0] += time.time() - attendance.vc_attendance[member][1]

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message == attendance.attendanceMsg and attendance.track_text_attendance == 1 and 'Student' in [role.name for role in user.roles]:
        attendance.attendees.add(user)

#Say hi!
@bot.command()
async def hello(ctx):
        await ctx.send('Hello!')
    
#Start recording attendance by reacting to a text message
@bot.command()
async def textattendance(ctx):
    if attendance.track_voice_attendance == 1:
        ctx.send('Already tracking attendance in the voice channel!')
        return
    if attendance.track_text_attendance:
        ctx.send('Already put up an attendance poll!')
        return
    attendance.track_text_attendance = 1
    embedAtt = discord.message.Embed()
    embedAtt.set_author(name='scoothBot')
    embedAtt.description = 'Tap the 🖐 below to mark your attendace!'
    attendance.attendanceMsg = await ctx.send(embed=embedAtt)
    await attendance.attendanceMsg.add_reaction('🖐')

#Show the recorded attendance
@bot.command()
async def showattendance(ctx, arg=''):
        if attendance.track_text_attendance == 0 and attendance.track_voice_attendance == 0:
            await ctx.send('Attendance hasn\'t been recorded, use $textattendance to start an attendance poll or $meetattendance to track voice channel attendance')
            return

        if arg == 'csv':
            attendanceStr = 'ATTENDEES\n'
        else:
            attendanceStr = '✅**ATTENDEES**✅\n'

        if attendance.track_text_attendance:
            people = attendance.attendees
        else:
            people = attendance.vc_attendance

        for attendee in people:
            if attendee.nick:
                if attendance.track_text_attendance:
                    attendanceStr += f'{attendee.nick}\n'
                else:
                    attendanceStr += f'{attendee.nick}, {prettier_time(people[attendee][0])}'
            else:
                if attendance.track_text_attendance:
                    attendanceStr += f'{attendee.display_name}\n'
                else:
                    attendanceStr += f'{attendee.display_name}, {prettier_time(people[attendee][0])}'
        
        if arg == 'csv':
            attendanceStr += '\nABSENTEES\n'
        else:
            attendanceStr += '\n❌**ABSENTEES**❌\n'
        for member in ctx.message.guild.members:
            if member not in people:
                for role in member.roles:
                    if role.name == 'Student':
                        if member.nick:
                            attendanceStr += f'{member.nick}\n'
                        else:
                            attendanceStr += f'{member.display_name}\n'
        
        if arg == 'csv':
            fp = open('Attendance.csv', 'w', encoding='utf-8')
            fp.write(attendanceStr)
            fp.close()
            sendFile = discord.File('Attendance.csv')
            await ctx.send(file=sendFile)
            
        else:
            await ctx.send(attendanceStr)
    
    
#Reset the attendance object to the initial condition
@bot.command()
async def clearattendance(ctx):
        attendance.track_text_attendance = 0
        attendance.reset()
        await ctx.send('Cleared attendance!🙌')

# Record the attendance in a voice channel
@bot.command()
async def meetattendance(ctx):
    if attendance.track_text_attendance:
        ctx.send('Already tracking attendance on a text channel')
        return
    if attendance.track_voice_attendance:
        ctx.send(f'Already tracking attendance in `{attendance.classroom_vc.name}`')
        return
    attendance.track_voice_attendance = 1
    sender = ctx.message.author
    channel = None
    for vc in ctx.message.guild.voice_channels:
        if sender in vc.members:
            channel = vc
            break
    if channel is None:
        await ctx.send('You\'re not in a voice channel!🤨')
    else:
        attendance.classroom_vc = channel
        for member in channel.members:
            attendance.vc_attendance[member] = [0, time.time()]
        await ctx.send(f'Tracking attendance in `{channel.name}`✅')

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
        
keyfile = open('clientkey.txt')
TOKEN = keyfile.readline()
bot.run(TOKEN)

