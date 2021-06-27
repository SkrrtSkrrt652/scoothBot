from inspect import Attribute
import discord
from discord import embeds
from discord.ext.commands import Bot
from discord.ext import commands
import time
import requests
import json
import random
import quick_search

import Classroom
import cringe
import search

intents = discord.Intents.all()
bot = Bot(command_prefix='$', intents=intents)

attendance = Classroom.Attendance()
quiz = Classroom.PopQuiz()

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
    if quiz.thrown and reaction.message == quiz.quizMessage and 'Student' in [role.name for role in user.roles]:
        if quiz.questions[quiz.current_qn][2] == quiz.optionEmojis.index(reaction.emoji):
            quiz.correct +=1
        quiz.total += 1


#Say hi!
@bot.command()
async def hello(ctx):
        await ctx.send('Hello!')
    
#Start recording attendance by reacting to a text message
@bot.command()
async def att(ctx, arg='', arg2=''):
    if arg == '':
        await ctx.send('Usage: $attendance <action> [save] (action = poll, voice, show, clear)')
        return
    elif arg == 'poll':
        if attendance.track_voice_attendance == 1:
            await ctx.send('Already tracking attendance in the voice channel!')
            return
        if attendance.track_text_attendance:
            await ctx.send('Already put up an attendance poll!')
            return
        attendance.track_text_attendance = 1
        embedAtt = discord.message.Embed()
        embedAtt.set_author(name='scoothBot')
        embedAtt.description = 'Tap the 🖐 below to mark your attendace!'
        attendance.attendanceMsg = await ctx.send(embed=embedAtt)
        await attendance.attendanceMsg.add_reaction('🖐')

    elif arg == 'show':
        if attendance.track_text_attendance == 0 and attendance.track_voice_attendance == 0:
            await ctx.send('Attendance hasn\'t been recorded, use $textattendance to start an attendance poll or $meetattendance to track voice channel attendance')
            return

        if arg2 == 'save':
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
                    if attendee in attendance.classroom_vc.members:
                        extra_time = time.time() - people[attendee][1]
                    else:
                        extra_time = 0
                    attendanceStr += f'{attendee.nick}, {prettier_time(people[attendee][0] + extra_time)}'
            else:
                if attendance.track_text_attendance:
                    attendanceStr += f'{attendee.display_name}\n'
                else:
                    if attendee in attendance.classroom_vc.members:
                        extra_time = time.time() - people[attendee][1]
                    else:
                        extra_time = 0
                    attendanceStr += f'{attendee.display_name}, {prettier_time(people[attendee][0] + extra_time)}'
        
        if arg2 == 'save':
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
        
        if arg2 == 'save':
            fp = open('Attendance.csv', 'w', encoding='utf-8')
            fp.write(attendanceStr)
            fp.close()
            sendFile = discord.File('Attendance.csv')
            await ctx.send(file=sendFile)
            
        else:
            await ctx.send(attendanceStr)
    
    elif arg == 'clear':
        attendance.track_text_attendance = 0
        attendance.reset()
        await ctx.send('Cleared attendance!🙌')

    elif arg == 'voice':
        if attendance.track_text_attendance:
            await ctx.send('Already tracking attendance on a text channel')
            return
        if attendance.track_voice_attendance:
            await ctx.send(f'Already tracking attendance in `{attendance.classroom_vc.name}`')
            return
        attendance.track_voice_attendance = 1
        sender = ctx.message.author
        channel = None
        for vc in ctx.message.guild.voice_channels:
            if sender in vc.members:
                channel = vc
                break
        if channel is None:
            attendance.track_voice_attendance = 0
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

#The pop quiz commands

@bot.command()
@commands.has_role('Teacher')
async def popquiz(ctx, arg1='', arg2=''):
    teacher = ctx.message.author
    if arg1 == '':
       await ctx.send('Usage: $popquiz <action> (action=create to create a quiz)')
    if arg1 == 'create':    
        if teacher.dm_channel is None:
            tch_dmc = await teacher.create_dm()
        else:
            tch_dmc = teacher.dm_channel
        
        await ctx.send('Okay! Check your DMs 👀')
        await tch_dmc.send('Hi! Let\'s create that pop quiz\nSend a csv/txt file with each line reperesenting a question in the format\n<question>, <option_1>, <option_2>, [option_3],...\nTwo options are mandatory, although you can use upto 8.')
        fileMessage = await bot.wait_for('message', check= lambda msg: len(msg.attachments) != 0  and msg.channel == tch_dmc)
        print(fileMessage.attachments)
        await fileMessage.attachments[0].save('quiz.csv')
        with open('quiz.csv') as quizFile:
            quiz.parse(quizFile)
        await tch_dmc.send('Okay! Your quiz is ready. Now you can use $popquiz throw [qno] in the server to throw a question that students can respond to. if [qno] is not given, a random question will be chosen!')
        
    if arg1 == 'throw':
        if quiz.thrown:
            await ctx.send("Reveal the answer to the previous question before throwing another one! Use $popquiz reveal")
            return
        quiz.thrown = 1

        if arg2 == '':
            quiz.current_qn = random.randrange(0, len(quiz.questions))
            question = quiz.questions[quiz.current_qn]
        else:
            if int(arg2) >= 0 and int(arg2) < len(quiz.questions):
                question = quiz.questions[int(arg2)]
                quiz.current_qn = int(arg2)
            else:
                await ctx.send('[qno] received an invalid response')
        qEmbed = discord.message.Embed(title = 'POP QUIZ')
        if teacher.nick:
            qEmbed.set_author(name=teacher.nick)
        else:
            qEmbed.set_author(name=teacher.display_name)
        qEmbed.add_field(name='Q', value=question[0], inline=False)
        for i in range(len(question[1])):
            qEmbed.add_field(name=quiz.optionEmojis[i], value=question[1][i], inline=False)
        questionMsg = await ctx.send(embed=qEmbed)
        quiz.quizMessage = questionMsg
        for i in range(len(question[1])):
            await questionMsg.add_reaction(f'{quiz.optionEmojis[i]}')

    if arg1 == 'reveal':
        if not quiz.thrown:
            await ctx.send("No question thrown. Throw one using $popquiz throw [qno]")
        else:
            quiz.thrown = 0
        ans_id = quiz.questions[quiz.current_qn][2]
        await ctx.send(f'**THE CORRECT ANSWER WAS {quiz.optionEmojis[ans_id]}{quiz.questions[quiz.current_qn][1][ans_id]}**')
        await ctx.send(f'{quiz.total} attempted the question, and {quiz.correct}({int(quiz.correct/quiz.total*100)}%) got it right!')
        quiz.total = 0
        quiz.correct = 0




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


@bot.command()
async def qsearch(ctx, query,number):
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
        
keyfile = open('clientkey.txt')
TOKEN = keyfile.readline()
bot.run(TOKEN)

