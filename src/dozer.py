
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
import asyncio

# Import private tokens from environment file
from dotenv import load_dotenv
load_dotenv()
DOZER_TOKEN = os.getenv('DOZER_TOKEN')
GUILD_NAME = os.getenv('TEST_SERVER_NAME')


client = discord.Client()

# Checks every minute whether it's time to trigger an event
async def time_check_task():
	await client.wait_until_ready();
	channel = client.get_channel(int('1069008079649251379'));
	while True:
		#print('Test')
		await channel.send('Test');
		await asyncio.sleep(10)

# Called once when client successfully connects and pulls client data
@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD_NAME:
			print(f'{client.user} has connected to ' + f'{GUILD_NAME}')
			client.loop.create_task(time_check_task())


client.run(DOZER_TOKEN)

# python ./src/dozer.py