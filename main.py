from inspect import Attribute
import discord
from discord.ext.commands import Bot
import time

import Classroom

intents = discord.Intents.all()
attendance = Classroom.Attendance() 

def prettier_time(time):
    time = int(time)
    if time < 60:
        return f'{time}s\n'
    elif time // 60 < 60:
        return f'{time//60}m {time % 60}s\n'
    else:
        return f'{time//3600}h {(time % 3600) // 60}m\n'


bot = Bot(command_prefix='$', intents=intents)

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


        
keyfile = open('clientkey.txt')
TOKEN = keyfile.readline()
bot.run(TOKEN)