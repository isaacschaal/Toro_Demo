import schedule
import time
import subprocess
from datetime import datetime

def main_monday():
    commands = ['nohup','python3', 'main_monday.py', '--d', str(datetime.today().strftime('%Y-%m-%d'))]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    print (process.stdout)

def main_friday():
    commands = ['nohup','python3', 'main_friday.py', '--d', str(datetime.today().strftime('%Y-%m-%d'))]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    print (process.stdout)


schedule.every().day.at("09:00").do(main_monday)
schedule.every().day.at("07:00").do(main_friday)


while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
