
# Dozer
# 01.28.2023
# Xephorium
# 
# A discord bot to enforce my sleep schedule. Dozer sends a 15 min warning via
# private message that bedtime is approaching. Then, when the time comes, it kicks
# me from VC and sends a pleasant message in the appropriate voice channel.
#
# To Run: python ./src/dozer.py

import os
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import random


#--- Variables ---#

# Import private tokens from environment file
from dotenv import load_dotenv
load_dotenv()
DOZER_TOKEN = os.getenv('DOZER_TOKEN')
GUILD_NAME = os.getenv('TEST_SERVER_NAME')
PERSONAL_DISCORD_ID = os.getenv('PERSONAL_DISCORD_ID')
PERSONAL_DISCORD_NAME = os.getenv('PERSONAL_DISCORD_NAME')

BACKGROUND_LOOP_DELAY = 5          # Seconds
BEDTIME               = 19*60 + 9  # Minutes
BEDTIME_WARNING       = 1          # Minutes


#--- Functions ---#

async def send_bedtime_warning():
	channel = client.get_channel(int('1069008079649251379'));
	await channel.send(':hourglass:');

def get_pleasant_message():
	return random.choice([
		f'{PERSONAL_DISCORD_NAME} is gone. Reduced to atoms.',
		f'{PERSONAL_DISCORD_NAME} has been banished to the shadow realm.',
		f'{PERSONAL_DISCORD_NAME} blasting off agaiiiiin! *(twinkle)*',
		f'You got 99 problems but {PERSONAL_DISCORD_NAME} ain\'t one.'
		]);

async def enforce_bedtime():
	for guild in client.guilds:
		for member in guild.members:
			if member.id == int(PERSONAL_DISCORD_ID):
				if member.voice is not None:
					channel = client.get_channel(member.voice.channel.id);
					await channel.send(get_pleasant_message());
					print('Removing ' + f'{member.name} (' + f'{member.id})')
					await member.move_to(None)

async def check_time():
	present = (datetime.now().hour * 60) + datetime.now().minute
	if present == BEDTIME - BEDTIME_WARNING:
		await send_bedtime_warning();
	if present == BEDTIME:
		await enforce_bedtime();

async def background_loop():
	await client.wait_until_ready();
	while True:
		await check_time();
		await asyncio.sleep(BACKGROUND_LOOP_DELAY)


#--- Main Program ---#

intents = discord.Intents().all()
client = commands.Bot(command_prefix = '?',intents=intents)

# Called once when client successfully connects and pulls client data
@client.event
async def on_ready():
	client.loop.create_task(background_loop())

client.run(DOZER_TOKEN, log_handler=None)

# python ./src/dozer.py