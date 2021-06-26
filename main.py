import discord
import Classroom

client = discord.Client()
attendance = Classroom.Attendance() 

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        if message.embeds:
            attendance.attendanceMsg = message
            if message.embeds[0].description == 'Tap the 🖐 below to mark your attendace!':
                await message.add_reaction('🖐')
        return

    #Say hi!
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    #Start recording attendance by reacting to a text message
    if message.content.startswith('$textattendance'):
        attendance.text_attendance = 1
        embedAtt = discord.message.Embed()
        embedAtt.set_author(name='scoothBot')
        embedAtt.description = 'Tap the 🖐 below to mark your attendace!'
        await message.channel.send(embed=embedAtt)

    #Show the recorded attendance
    if message.content.startswith('$showattendance'):
        if attendance.text_attendance == 0:
            await message.channel.send('Attendance hasn\'t been recorded, use $textattendance to start an attendance poll')
            return
        attendanceStr = '**ATTENDEES**\n'
        for attendee in attendance.attendees:
            if attendee.nick:
                attendanceStr += f'{attendee.nick}\n'
            else:
                attendanceStr += f'{attendee.display_name}\n'
        attendanceStr += '**ABSENTEES**\n'
        for member in message.guild.members:
            if member not in attendance.attendees:
                for role in member.roles:
                    if role.name == 'Student':
                        if member.nick:
                            attendanceStr += f'{member.nick}\n'
                        else:
                            attendanceStr += f'{member.display_name}\n'
        await message.channel.send(attendanceStr)
    
    #Reset the attendance object to the initial condition
    if message.content.startswith('$clearattendance'):
        attendance.text_attendance = 0
        attendance.reset()
        await message.channel.send('Cleared attendance!')
        

@client.event
async def on_voice_state_update(member, before, after):
    channel = after.channel

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message == attendance.attendanceMsg and attendance.text_attendance == 1 and 'Student' in [role.name for role in user.roles]:
        attendance.attendees.add(user)
        

client.run('ODU3NTU2ODAwMDAxNTQwMTE3.YNRUAQ.SwFfqIzS_Y5AN8TRNZSnxzA33RI')