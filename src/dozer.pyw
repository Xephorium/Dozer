
# Dozer
# 01.28.2023
# Xephorium
# 
# A discord bot to enforce my sleep schedule. Dozer sends a 15 min warning via
# private message that bedtime is approaching. Then, when the time comes, it kicks
# me from VC and sends a pleasant message in the appropriate voice channel.
#
# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1069006318620377158&permissions=16779264&scope=bot
#
# To Run: python ./src/dozer.py

import os
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import random
import os


#--- Variables ---#

# Import private tokens from environment file
from dotenv import load_dotenv
load_dotenv();
DOZER_TOKEN = os.getenv('DOZER_TOKEN');
DISCORD_ID_LIST = os.environ.get("DISCORD_ID_LIST").split(".");
BEDTIME_WEEKDAY_LIST = os.environ.get("BEDTIME_WEEKDAY_LIST").split(".");
BEDTIME_WEEKEND_LIST = os.environ.get("BEDTIME_WEEKEND_LIST").split(".");

# Define Constants
EARLY_MORNING_DAY_TRANSITION = 300; # 5am CST
BACKGROUND_LOOP_DELAY = 60;         # In Seconds
BEDTIME_WARNING       = 10;         # In Minutes
BEDTIME_FOLLOWUP      = 10;         # In Minutes


#--- Functions ---#

async def send_bedtime_warning(index):
	for guild in client.guilds:
		for member in guild.members:
			if member.id == int(DISCORD_ID_LIST[index]):
				if member.voice is not None:
					channel = await member.create_dm();
					await channel.send(f'{BEDTIME_WARNING}mins \'till bedtime :hourglass:');

def get_pleasant_message(name):
	random.seed(os.urandom(10), 1);
	return random.choice([
		f'{name} is gone. Reduced to atoms.',
		f'{name} has been banished to the shadow realm.',
		f'{name} is blasting off agaiiiiin! *(twinkle)*',
		f'You got 99 problems but {name} ain\'t one.',
		f'{name} doesn\'t have to go home, but they can\'t stay here.',
		f'Nothing personal, {name}. *(teleports behind them)*',
		f'{name} is sleepin\' with the fishies.',
		f'{name} is countin\' sheep.',
		f'{name} has a meeting with \'Ole Lukøje.',
		f'Future {name} will appreiate present {name}\'s good judgement.',
		f'No respectable Palian should be awake at this hour, {name}.',
		]) + f'\n\nᴵ ᵏᶦᶜᵏ ᵗʰᵉ ˢᵒᶜᶦᵃˡˡʸ ᵐᵃˡˡᵉᵃᵇˡᵉ ᵗᵒ ᵉⁿᶠᵒʳᶜᵉ ᵗʰᵉᶦʳ ᵇᵉᵈᵗᶦᵐᵉˢ';

async def enforce_bedtime(index):
	for guild in client.guilds:
		for member in guild.members:
			if member.id == int(DISCORD_ID_LIST[index]):
				if member.voice is not None:
					channel = client.get_channel(member.voice.channel.id);
					await channel.send(get_pleasant_message(member.name));
					await member.move_to(None);

def get_late_night_weekday(present):
	# Account for 5 hours into the early morning of the next day
	if (present < EARLY_MORNING_DAY_TRANSITION):
		return (datetime.now().weekday() - 1) % 6;
	else:
		return datetime.now().weekday()

def is_weekday(present):
	# Check whether Friday or Saturday night
	# M T W T F S S
	# 0 1 2 3 4 5 6
	late_night_day = get_late_night_weekday(present);
	if (late_night_day == 4 or late_night_day == 5):
		return False;
	else:
		return True;

async def check_time():
	present = (datetime.now().hour * 60) + datetime.now().minute;
	for index in range(len(DISCORD_ID_LIST)):
		if is_weekday(present):
			if (BEDTIME_WEEKDAY_LIST[index] != '-'):
				if present == int(BEDTIME_WEEKDAY_LIST[index]) - BEDTIME_WARNING:
					await send_bedtime_warning(index);
				if present == int(BEDTIME_WEEKDAY_LIST[index]):
					await enforce_bedtime(index);
				if present == int(BEDTIME_WEEKDAY_LIST[index]) + BEDTIME_FOLLOWUP:
					await enforce_bedtime(index);
		else:
			if (BEDTIME_WEEKEND_LIST[index] != '-'):
				if present == int(BEDTIME_WEEKEND_LIST[index]) - BEDTIME_WARNING:
					await send_bedtime_warning(index);
				if present == int(BEDTIME_WEEKEND_LIST[index]):
					await enforce_bedtime(index);
				if present == int(BEDTIME_WEEKEND_LIST[index]) + BEDTIME_FOLLOWUP:
					await enforce_bedtime(index);

async def background_loop():
	await client.wait_until_ready();
	while True:
		await check_time();
		await asyncio.sleep(BACKGROUND_LOOP_DELAY);


#--- Main Program ---#

intents = discord.Intents().all();
client = commands.Bot(command_prefix = '?',intents=intents);

# Called once when client successfully connects and pulls client data
@client.event
async def on_ready():
	client.loop.create_task(background_loop());

client.run(DOZER_TOKEN, log_handler=None);