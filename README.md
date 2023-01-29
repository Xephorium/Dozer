<img align="left" width="120" src="res/Dozer Icon GitHub.png" alt="Dozer Icon">

# Dozer
A discord bot to enforce my sleep schedule. 

</br>

### Project Setup
1. Install Python w/ pip (included by default)
2. Download discord library: `pip install -U discord.py`
3. Download dotenv library: `pip install -U python-dotenv`
4. [Create & setup a new bot](https://realpython.com/how-to-make-a-discord-bot-python/) in the [Discord Developer Portal](https://discord.com/developers/applications)
4. Create the data file (details below)
5. Run bot: `python ./src/dozer.py`

### Data File
Running Dozer requires a file be added in the same directory as `dozer.py`. This file is called `.env` and contains the private tokens and server data needed to put you (and your friends) to bed. The format of `.env` should be as follows:
```
# Token created on the Discord Developer Portal
DOZER_TOKEN=<bot token>

# List of unique user ID's to enforce, separated by '.'
DISCORD_ID_LIST='<discord user 1 token>.<discord user 2 token>'

# Bedtimes, in same order as users. '.' delimiter. '-' for no bedtime.
BEDTIME_WEEKDAY_LIST='<weekday bedtime for user 1>.<weekday bedtime for user 2>'
BEDTIME_WEEKEND_LIST='<weekend bedtime for user 1>.-'
```
