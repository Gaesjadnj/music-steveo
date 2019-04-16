import discord
from discord.ext.commands import Bot
from discord.ext import commands
import youtube_dl
import asyncio
import queue
import time
import json
import random
import inspect
import datetime
import os
from discord import Game
from discord.utils import get

Client = discord.client
client = commands.Bot(command_prefix = 'bq.')
Clientdiscord = discord.Client()
evn=client.event
cms=client.command(pass_context=True)

async def picker():
    mem_watching=['{} Users']
    mem_watching=['Biquest']
    mem_listening=['{} Users']
    mem_playing=['Need upvotes to grow!']
    ser_watch=['{} servers']
    ser_listen=['Steveo']
    ser_play=['bq.help | v1.0']
    helps=['!help | for help','!help for help commands']

    while True:
        kind=random.randint(1,2)
        if kind == 1:
            members=0
            for i in client.servers:
                members+=len(i.members)
            num = random.choice([1, 2, 3])
            if num == 1:
                await client.change_presence(game=discord.Game(name=random.choice(mem_playing).format(members), type=1))
            if num == 2:
                await client.change_presence(game=discord.Game(name=random.choice(mem_listening).format(members), type=2))
            if num == 3:
                await client.change_presence(game=discord.Game(name=random.choice(mem_watching).format(members), type=3))
            await asyncio.sleep(random.choice([10, 10, 10, 10, 10, 10]))

        if kind == 2:
            num = random.choice([1, 2, 3])
            if num == 1:
                await client.change_presence(game=discord.Game(name=random.choice(ser_play).format(len(client.servers)), type=1))
            if num == 2:
                await client.change_presence(game=discord.Game(name=random.choice(ser_listen).format(len(client.servers)), type=2))
            if num == 3:
                await client.change_presence(game=discord.Game(name=random.choice(ser_watch).format(len(client.servers)), type=3))
            await asyncio.sleep(random.choice([10, 10, 10, 10, 10, 10]))

        if kind == 3:
            await client.change_presence(game=discord.Game(name=random.choice(ser_watch).format(len(client.servers)), type=3))
            await asyncio.sleep(random.choice([10, 10, 10, 10, 10, 10]))

@client.event
async def on_ready():
    client.loop.create_task(picker())
    print("{} has successfully booted and running!".format(client.user.name))

players = {}
queues= {}
 
def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start() 
 
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say('I have joined the `voice channel`')
 
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say('I have left the Voice Channel!')
 
@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()
    await client.say('I started playing the video!')
 
@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    await client.say('I have paused the video!')
    
@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    await client.say('I have resumed the video!')
    
@client.command(pass_context=True)
async def skip(ctx):
    id = ctx.message.server.id
    players[id].skip()
    await client.say('I have skipped the video!')
    
@client.command
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
 
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('I have added the video in the queue!')
 
@client.command()
async def help1():
    embed = discord.Embed(
        title = 'Help',
        description = 'Help Page For All Of The Commands!',
        )
    embed.add_field(name='bqm.join', value='Makes the bot join the Voice Channel', inline=False)
    embed.add_field(name='bqm.leave', value='Makes the bot leave the Voice Channel', inline=False)
    embed.add_field(name='bqm.play', value='Makes the bot play a YouTube video', inline=False)
    embed.add_field(name='bqm.pause', value='Makes the bot pause the Video', inline=False)
    embed.add_field(name='bqm.resume', value='Makes the bot resume the Video', inline=False) 
    embed.add_field(name='bqm.skip', value='Makes the bot skip the Video', inline=False)
    embed.add_field(name='bqm.queue', value='Makes the bot queue a Video', inline=False)
    await client.say(embed=embed)

client.remove_command('help')

@client.command(name="kick", pass_context=True)
async def _kick(ctx, user: discord.Member = None, *, arg = None):
    if ctx.message.author.server_permissions.kick_members == True:
        if user is None:
            await client.say(":x: Error. You haven't defined a user to kick. Try again")	
            return False
        if arg is None:
            await client.say("Please provide a reason to kick {}".format(user.name))
            return False
        reason = arg
        author = ctx.message.author
        await client.kick(user)
        embed = discord.Embed(title="Kick", description=" ", color=0xffffff)
        embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
        embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
        embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
        await client.say(embed=embed)
    else:
    	await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `kick members`.".format(ctx.message.author.mention))


@client.command(name="ban", pass_context=True)
async def _ban(ctx, user: discord.Member = None, *, arg = None):
    if ctx.message.author.server_permissions.ban_members == True:
        if user is None:
            await client.say(":x: No user defined")
            return False
        if arg is None:
            await client.say("Please provide a reason to ban {}".format(user.name))
            return False
        reason = arg
        author = ctx.message.author
        await client.ban(user)
        embed = discord.Embed(title="Ban", description=" ", color=0xFF0000)
        embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
        embed.add_field(name="By: ", value="{}".format(author.mention), inline=False)
        embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/551995766189850634/564253818657701888/Fade_image.png")
        await client.say(embed=embed)
    else:
    	await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `ban members`.".format(ctx.message.author.mention))

@client.command(name="mute", pass_context=True)
async def _mute(ctx, user: discord.Member = None, *, arg = None):
    if ctx.message.author.server_permissions.manage_messages == True:
        if user is None:
            await client.say(":x: No user defined for ``.mute``.")
            return False
        if arg is None:
            await client.say("Please provide a reason to mute **{}**".format(user.name))
            return False
        reason = arg
        author = ctx.message.author
        role = discord.utils.get(ctx.message.server.roles, name="Muted")
        await client.add_roles(user, role)
        embed = discord.Embed(title="Mute", description=" ", color=0xFFA500)
        embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
        embed.add_field(name="By: ", value="{}".format(author.mention), inline=False)
        embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/551995766189850634/564253818657701888/Fade_image.png")	
        await client.say(embed=embed)
    else:
    	await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `manage messages`.".format(ctx.message.author.mention))


@client.command(name="warn", pass_context=True)
async def _warn(ctx, user: discord.Member = None, *, arg = None):
    if ctx.message.author.server_permissions.manage_messages == True:
        if user is None:
            await client.say(":x: No user defined")
            return False
        if arg is None:
            await client.say("please provide a reason to {}".format(user.name))
            return False
        reason = arg
        author = ctx.message.author
        server = ctx.message.server
        embed = discord.Embed(title="Warn", description=" ", color=0x00ff00)
        embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
        embed.add_field(name="By: ", value="{}".format(author.mention), inline=False)
        embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
        await client.say(embed=embed)
        em = discord.Embed(description=" ", color=0x00ff00)
        em.add_field(name="you have been warned for: ", value=reason)
        em.add_field(name="\nfrom:", value=server)
        await client.send_message(user, embed=em)
    else:
    	await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `manage messages`.".format(ctx.message.author.mention))

@client.command(name="removewarn", pass_context=True)
async def _removewarn(ctx, user: discord.Member = None, *, arg = None):
    if ctx.message.author.server_permissions.manage_messages == True:
        if user is None:
            await client.say(":x: No user defined to unwarn")
            return False
        if arg is None:
            await client.say("Please provide a reason to unwarn {}".format(user.name))
            return False
        reason = arg
        author = ctx.message.author
        role = discord.utils.get(ctx.message.server.roles, name="Muted")
        await client.remove_roles(user, role)
        embed = discord.Embed(title="Unwarn", description=" ", color=0x00ff00)
        embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
        embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
        embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/551995766189850634/564253818657701888/Fade_image.png")
        await client.say(embed=embed)
    else:
    	await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `manage_messages`.".format(ctx.message.author.mention))

@client.event
async def on_member_join(user):
    embed=discord.Embed(description=f'<a:warning:557215838294507520> {user.name} has joined a server!')
    embed.add_field(name='<:member:556962083426795526> Member',value=user.name)
    embed.add_field(name='<:member:556962083426795526> Member ID',value=user.id)
    embed.add_field(name=':robot: Bot Account',value=user.client)
    embed.add_field(name='<:member:556962083426795526> Nickname',value=None)
    embed.add_field(name='<:member:556962083426795526> Avatar URL',value=user.avatar_url)
    embed.add_field(name='<:cog:553328079272017932> Top Role',value=user.top_role)
    embed.add_field(name='<:cog:553328079272017932> Server Name ',value=user.server.name)
    embed.set_footer(icon_url=user.avatar_url,text=user.joined_at)
    await client.send_message(discord.Object(id='556971586230550549'),embed=embed)

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)


async def eightball(context):
    possible_responses = [
        'That is a certain no',
        'It is not looking likely',
        'Too hard to tell',
        'It is a possibility',
        'Definitely',
	'Certainly',
	'No',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.command(pass_context=True)
async def slay(ctx, *, member: discord.Member = None):

    try:
        if member is None:
            await client.say(ctx.message.author.mention + " has been killed!")
        else:
            if member.id == ctx.message.author.id:
                await client.say(ctx.message.author.mention + " took their own life")
            else:
                embed=discord.Embed(description=member.mention + " has been killed by " + ctx.message.author.mention + "!")
                embed.set_image(url="https://cdn.travelpulse.com/images/99999999-9999-9999-9999-999999999999/749e785f-d3ef-e611-9aa9-0050568e420d/630x355.jpeg")
                await client.say(embed=embed)
    except:
        pass


@client.command(pass_context=True)
async def broadcast(ctx, *, msg):
    if ctx.message.author.id == "341933833136111617":
        for server in client.servers:
            for channel in server.channels:
                await client.send_message(channel, msg)
    else:
        pass

@client.command(pass_context = True)
async def bans(ctx):
    if ctx.message.author.server_permissions.ban_members == True:
        x = await client.get_bans(ctx.message.server)
        x = '\n'.join([y.name for y in x])
        embed = discord.Embed(title = "Ban list", description = x, color = 0xffffff)
        return await client.say(embed = embed)
        channel = client.get_channel('543488075809030145')
        embed = discord.Embed(title=f"User: {ctx.message.author.name} have used bans command", description=f"User ID: {ctx.message.author.id}", color=0xff9393)
        await client.send_message(channel, embed=embed)
    else:
        await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `ban members`.".format(ctx.message.author.mention))

@client.command(name="clear", pass_context=True)
async def _clear(ctx, amount=100):
    if ctx.message.author.server_permissions.manage_messages == True:
        channel = ctx.message.channel
        messages = [ ]
        async for message in client.logs_from(channel, limit=int(amount) + 1):
            messages.append(message)
        await client.delete_messages(messages)
        msg = await client.say(f"{amount} messages has been deleted.")
        await asyncio.sleep(5)
        await client.delete_message(msg)
        channel = client.get_channel('543488075809030145')
        embed = discord.Embed(title=f"User: {ctx.message.author.name} have used clean command", description=f"User ID: {ctx.message.author.id}", color=0xffffff)
        await client.send_message(channel, embed=embed)
    else:
    	await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `manage messages`.".format(ctx.message.author.mention))

@client.command(name='eval', pass_context=True)
async def _eval(ctx, *, command):
    if ctx.message.author.id == "457214181268127747" or "341933833136111617" or "305093302561144833":
        res = eval(command)
        if inspect.isawaitable(res):
            await client.say(await res)
        else:
            await client.send_typing(ctx.message.channel)
            await asyncio.sleep(3)
            await client.say(res)
    else:
        await client.send_typing(ctx.message.channel)
        await asyncio.sleep(1)
        await client.delete_message(msg)
        await client.delete_message(ctx.message)
        await asyncio.sleep(0.5)
        await client.delete_message(m)
        await client.send_message(ctx.message.channel, "Sorry {} You have no permission to use this command only the bot owners can use this.".format(ctx.message.author.mention))

@client.command(pass_context=True)
async def stats(ctx):
	author = ctx.message.author
	servers = list(client.servers)
	embed = discord.Embed(description="Invite Biquest today!!! :thumbsup: with a lot of fun commands along with some moderational commands! Updated weekly adding new features, memes, kill command, and TONS MORE!!!", color=0xFFFF)
	embed.add_field(name="Servers:", value=f"{} Pro Servers")
	embed.add_field(name="Users:", value=f"{} Users")
	embed.add_field(name="Invite", value=f"[Link](https://discordapp.com/oauth2/authorize?&client_id=548803611535343626&scope=bot&permissions=8)")
	embed.add_field(name="Support server", value=f"[Link](https://discord.gg/rt2d8n4)")
	embed.add_field(name="Discord Server List", value=f"[Link](https://discordbots.org/bot/529463184910712872#)")
	embed.add_field(name="Memory", value="Free: 10.40GB / Total: 20.80GB",inline=True)
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/554925878983786496/564029266971459604/705f3f54badfeb6d81593237dc6168fe.png")
	embed.set_footer(text=" | {}".format(client.user.name), icon_url="https://cdn.discordapp.com/attachments/554925878983786496/564029266971459604/705f3f54badfeb6d81593237dc6168fe.png")
	await client.say(embed=embed)
	channel = client.get_channel('543488075809030145')
	embed = discord.Embed(title=f"User: {ctx.message.author.name} have used stats command", description=f"User ID: {ctx.message.author.id}", color=0xffffff)
	embed.set_image(url="http://www.clipartsuggest.com/images/198/the-world-of-truth-our-main-website-is-www-theworldoftruth-org-ref-I51NIK-clipart.gif")
	await client.send_message(channel, embed=embed)

@client.command(name="report", pass_context=True)
async def _report(ctx, user: discord.Member = None, *, arg = None):
    if ctx.message.author.server_permissions.send_messages == True:
        log_channel = discord.utils.get(ctx.message.server.channels, name = 'mod-log')
        if user is None:
            await client.say(":x: Error 302. Please mention a member")
            return False
        if arg is None:
            await client.say("please provide a reason for reporting {}".format(user.name))
            return False
        reason = arg
        author = ctx.message.author
        server = ctx.message.server
        channel = ctx.message.channel
        em = discord.Embed(title=f"{user} has been reported",description="", color=0xffffff)
        em.add_field(name="Reason:", value=reason,inline=True)
        em.add_field(name="User:", value=author,inline=True)
        em.add_field(name="In server:", value=server,inline=True)
        em.add_field(name="In Channel:", value=channel,inline=True)
        em.set_footer(text=f"{datetime.datetime.now()}")
        try:
            await client.send_message(log_channel, embed=em)
        except:
            await client.say("There doesn't seem to be a channel called `mod-log` in this server! Please create it and try again")
    else:
        await client.send_message(ctx.message.channel, "Sorry {}, You don't have requirement permission to use this command `manage messages`.".format(ctx.message.author.mention))

@client.event
async def on_message(message):
	if message.content.startswith('bq.verify'):
		embed=discord.Embed(description=f"Success {message.author.mention} you have been verified!\nTime verified: **{datetime.datetime.now()}**\nyou will receive your role in 2 hours.")
		embed.set_image(url="https://cdn.discordapp.com/attachments/551995766189850634/564253818657701888/Fade_image.png")    
		await client.send_message(message.channel, embed=embed)
	await client.process_commands(message)
                           
@client.event
async def on_member_join(member):
    time.sleep(7600)
    role = discord.utils.get(member.server.roles, name='Verified')
    await client.add_roles(member, role) 
    await client.say('Done! User role applied.')

@client.command(Pass_Context=True) 
async def invite():
    embed=discord.Embed(title="Invite Me", description="Invite Biquest today!", color=0xff0000)
    embed.set_author(name="Invite Biquest")
    embed.set_image(url="https://cdn.discordapp.com/attachments/562223102004822021/566626837518745601/7d9b1d662b28cd365b33a01a3d0288e1--robot-logo-design-logo-robot.jpg")
    embed.set_footer(text="Made By Steveo#5019") 
    embed.add_field(name="Invite", value=f"[Click here for Link](https://discordapp.com/oauth2/authorize?&client_id=548803611535343626&scope=bot&permissions=8)")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def unban(con,user:int):
    if con.message.author.server_permissions.ban_members == True:
        try:
            who=await client.get_user_info(user)
            await client.unban(con.message.server,who)
            await client.say("The user you wanted to ban has successfully been unbanned.")
        except:
            await client.say("Oh No, Something went wrong!!")
    else:
    	await client.send_message(con.message.channel, "Sorry {}, You don't have requirement permission to use this command `ban members`.".format(con.message.author.mention))

@client.command(pass_context=True)
async def google(ctx):
    """USES URBAN DICT TO FIND DEFINITION OF WORDS. EX: s.urban neko"""
    word = ctx.message.content[7:]
    link = 'http://urbandictionary.com/v0/define?term={}'.format(word)
    rq_link = rq.get(link).text
    rq_json = json.loads(rq_link)
    await client.say("Word: {}\nVotes: {}\nDefinitioin: {}\nExample: {}".format(rq_json['list'][0]['word'], rq_json['list'][0]['thumbs_up'], rq_json['list'][0]['definition'], rq_json['list'][0]['example']))

@client.listen("on_command_error")
async def on_command_error(error,con):
    data={
        "Author Name":con.message.author.name,
        "Author Id": con.message.author.id,
        "Channel name":con.message.channel.name,
        "Channel id": con.message.channel.id,
        "Server Name":con.message.server.name,
        "Server Id": con.message.server.id,
        "Command Used": str(error.args),
        "Message": con.message.content
    }
    emb=discord.Embed(title="Command Error")
    for i in data:
        emb.add_field(name=i,value=data[i])
    who=discord.utils.get(client.get_all_members(),id='341933833136111617')
    await client.send_message(who,embed=emb)

@client.command(pass_context=True, no_pm=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(description="You requested help? Here it is!",color=0xffffff)
    embed.add_field(name="Welcome to the help commands! ", value="If you need any help feel free to contact the person who added Graphiq#6148!")
    embed.add_field(name="__Fun Commands__", value="Fun commands for all users.", inline=True)
    embed.add_field(name="bq.slay (ping a user)", value="Kill a user", inline=False)
    embed.add_field(name="bq.thanks (ping a user)", value="Says Thank You in a gif", inline=False)
    embed.add_field(name="bq.ball (question)", value="Replyies to your question in a fun way", inline=False)
    embed.add_field(name="bq.square (number)", value="Square a number in Maths", inline=False)
    embed.add_field(name="bq.beg", value="Beg yourself", inline=False)
    embed.add_field(name="bq.truthordare", value="Truth or Dare! (WIP)", inline=False)
    embed.add_field(name="bq.diceroll", value="Roll the dice (WIP)", inline=False)
    embed.add_field(name="__Music Commands__", value="music commands to play in voice channel", inline=True)
    embed.add_field(name="bq.join", value="Joins the bot to voice channel", inline=False)
    embed.add_field(name="bq.play (youtube URL)", value="plays the URL suggested by the user.", inline=False)
    embed.add_field(name="bq.leave", value="Leaves the voice channel", inline=False)
    embed.add_field(name="bq.stop", value="Stops the current video being played", inline=False)
    embed.add_field(name="bq.resume", value="Resumes the video that has been stoped", inline=False)
    embed.add_field(name="bq.queue (youtube URL)", value="Queue's a video", inline=False)
    embed.add_field(name="__Moderation Commands__", value="Moderation Commands for specific permissions to use.", inline=True)
    embed.add_field(name="bq.report (user & reason)", value="Reports a user. Requries a channel called #mod-log", inline=False)
    embed.add_field(name="bq.mute (user & reason)", value="Mutes a user. Requries a role called Muted and above most roles. Decline all perms.", inline=False)
    embed.add_field(name="bq.kick (user & reason)", value="Kicks a user and displays in the same channel the Moderator, User and Reason.", inline=False)
    embed.add_field(name="bq.ban (user & reason)", value="Bans a user and displays the ban reason. ", inline=False)
    embed.add_field(name="bq.bans", value="Administrator+, can see all of the banned members in the server.", inline=False)
    embed.add_field(name="bq.clear", value="Manage Messages+, Clean a specific number of messages 98-.", inline=False)
    embed.add_field(name="bq.removewarn (user & reason)", value="Removes a warn from a user", inline=False)
    embed.add_field(name="bq.dm (user & reason)", value="Dm's a user", inline=False)
    embed.add_field(name="__Credits__", value="Credits to the following:", inline=True)
    embed.add_field(name="Steveo#5019", value="Head CEO of Biquest. Main Bot Developer.", inline=False)
    embed.add_field(name="blank#4342", value="Main Bot Helper", inline=False)
    await client.send_message(author, embed=embed)
    embed = discord.Embed(description=" ", color=0x002aff)
    m=await client.say(":thumbsup: check DM's")
    await asyncio.sleep(0.5)
    await client.delete_message(m)
    em=discord.Embed()
@client.command(pass_context = True)

async def dm(ctx, user: discord.Member, *, msg: str):
   if user is None or msg is None:
       await client.say('Invalid args. Use this command like: ``d?dm @user message``')
   if ctx.message.author.server_permissions.kick_members == False:
       await client.say('**You do not have permission to use this command**')
       return
   else:
       await client.send_message(user, msg)
       await client.delete_message(ctx.message)          
       await client.say("Success! Your DM has made it! :white_check_mark: ")



@client.command(pass_context = True)
async def setupwelcomer(ctx):
    if ctx.message.author.bot:
      return
    if ctx.message.author.server_permissions.administrator == False:
      await client.say('**You do not have permission to use this command**')
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, 'welcome',everyone)
      await client.say(':white_check_mark:**Success setup**')

async def thanks(ctx, *, member: discord.Member = None):
    try:
        if member is None:
            await client.say(ctx.message.author.mention + " has been thanked!")
        else:
            if member.id == ctx.message.author.id:
                await client.say(ctx.message.author.mention + " thanked his self! LOL")
            else:
                embed=discord.Embed(description=member.mention + " has been thanked by " + ctx.message.author.mention + "!")
                embed.set_image(url="https://media1.tenor.com/images/cc619912fe89d1ff0d496b9d8fae70a4/tenor.gif")
                await client.say(embed=embed)
    except:
        pass
client.run('NTQ4ODAzNjExNTM1MzQzNjI2.D1KozA.0m0NsR_NekPr9vmEM_MKr5xHxeQ')
