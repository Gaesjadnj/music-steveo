import discord
from discord.ext import commands
import asyncio
import requests, bs4
import os
import time
import youtube_dl
import inspect
import datetime
from discord import opus

start_time = time.time()

client = commands.Bot(command_prefix=("bq."))
songs = asyncio.Queue()
play_next_song = asyncio.Event()
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(game=Game(name='music'))
    print('Ready, Freddy') 

    players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()
    
async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()


def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)


@client.command(pass_context=True)
async def plays(ctx, url):
    if not client.is_voice_connected(ctx.message.server):
        voice = await client.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = client.voice_client_in(ctx.message.server)
        
        player = await voice.create_ytdl_player(url, after=toggle_next)
        await songs.put(player)
@client.command(pass_context=True, no_pm=True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
    
    
    
    
    
@client.command(name="join", pass_context=True, no_pm=True)
async def _join(ctx):
    user = ctx.message.author
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Successfully connected to voice channel:", value=channel)
    await client.say(embed=embed)
    
@client.command(name="leave", pass_context=True, no_pm=True)
async def _leave(ctx):
    user = ctx.message.author
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Successfully disconnected from:", value=channel)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def pause(ctx):
    user = ctx.message.author
    id = ctx.message.server.id
    players[id].pause()
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Player Paused", value=f"Requested by {ctx.message.author.name}")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def skip(ctx):
    user = ctx.message.author
    id = ctx.message.server.id
    players[id].stop()
    embed = discord.Embed(colour=user.colour)
    embed.add_field(name="Player Skipped", value=f"Requested by {ctx.message.author.name}")
    await client.say(embed=embed)
@client.command(name="play", pass_context=True)
async def _play(ctx, *, name):
    author = ctx.message.author
    name = ctx.message.content.replace("m.play ", '')
    fullcontent = ('http://www.youtube.com/results?search_query=' + name)
    text = requests.get(fullcontent).text
    soup = bs4.BeautifulSoup(text, 'html.parser')
    img = soup.find_all('img')
    div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
    a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
    title = (a[0]['title'])
    a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
    url = ('http://www.youtube.com'+a0['href'])
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    print("User: {} From Server: {} is playing {}".format(author, server, title))
    player.start()
    embed = discord.Embed(description="**__Song Play By MUZICAL DOCTORB__**")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/03/2b/08/032b0870b9053a191b67dc8c3f340345.gif")
    embed.add_field(name="Now Playing", value=title)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def queue(ctx, *, name):
    name = ctx.message.content.replace("m.queue ", '')
    fullcontent = ('http://www.youtube.com/results?search_query=' + name)
    text = requests.get(fullcontent).text
    soup = bs4.BeautifulSoup(text, 'html.parser')
    img = soup.find_all('img')
    div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
    a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
    title = (a[0]['title'])
    a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
    url = ('http://www.youtube.com'+a0['href'])
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    embed = discord.Embed(description="**__Song Play By MUZICAL DOCTORB__**")
    embed.add_field(name="Video queued", value=title)
    await client.say(embed=embed)

client.loop.create_task(audio_player_task())
client.run(os.environ['BOT_TOKEN']
