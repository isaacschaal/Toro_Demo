# This is the main script to run Toro
# It should be constantly running, via supervisord
# It handles the full generating, tweeting, and minting process
# The specific timing of generating and minting can be modified
# by changing the schedule.every()... commands (It can be set to
# run every day at different hours, or everyweek on different days, etc.)

# Imports
import schedule
import time
import subprocess
from datetime import datetime

# Run the main_generate.py script with subprocess
# Passes the current date
def main_generate():
    commands = ['nohup','python3', 'scripts/main_generate.py', '--d', str(datetime.today().strftime('%Y-%m-%d'))]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    print (process.stdout)

# Run the main_mint.py script with subprocess
# Passes the current date
def main_mint():
    commands = ['nohup','python3', 'scripts/main_mint.py', '--d', str(datetime.today().strftime('%Y-%m-%d'))]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    print (process.stdout)

# Schedule the minting to happen everyday at 07:00
# and the new artworks to be generated everyday at 09:00
schedule.every().day.at("09:00").do(main_generate)
schedule.every().day.at("07:00").do(main_mint)

# Check for scheduled events every minute
while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
