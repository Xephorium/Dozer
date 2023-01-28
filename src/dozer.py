
# Dozer
# 01.28.2023
# Xephorium
# 
# A discord bot to enforce my sleep schedule. Dozer sends a 15 min warning
# via private message that bedtime is approaching. Then, when the time comes,
# it kicks me from VC and sends a pleasant message explaining why I vanished.
#
# To Run: python ./src/dozer.py

import os
import discord
from datetime import datetime
import asyncio


#--- Variables ---#

# Import private tokens from environment file
from dotenv import load_dotenv
load_dotenv()
DOZER_TOKEN = os.getenv('DOZER_TOKEN')
GUILD_NAME = os.getenv('TEST_SERVER_NAME')

BEDTIME_IN_MINUTES = 17*60 + 54
BEDTIME_WARNING_IN_MINUTES = 1


client = discord.Client()

# Performs time check
async def check_time():
	present = (datetime.now().hour * 60) + datetime.now().minute
	if present == BEDTIME_IN_MINUTES - BEDTIME_WARNING_IN_MINUTES:
		await client.wait_until_ready();
		channel = client.get_channel(int('1069008079649251379'));
		await channel.send(':hourglass:');
	if present == BEDTIME_IN_MINUTES:
		await client.wait_until_ready();
		channel = client.get_channel(int('1069008079649251379'));
		await channel.send('Gone');

# Delegates time check once each minute
async def background_loop():
	while True:
		await check_time();
		await asyncio.sleep(10)

# Called once when client successfully connects and pulls client data
@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD_NAME:
			print(f'{client.user} has connected to ' + f'{GUILD_NAME}')
			client.loop.create_task(background_loop())


client.run(DOZER_TOKEN)

# python ./src/dozer.py