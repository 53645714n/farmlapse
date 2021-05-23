import os
import sys
import time
from datetime import datetime, timezone
from suntime import Sun
from config import config

def try_to_mkdir(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def prepare_dir(base):
    path = "pictures"
    try_to_mkdir(base + "/" +path)

    return path

def make_os_command(config, file_name):
    height = config["height"]
    width = config["width"]

    os_command = "/opt/vc/bin/raspistill -q "+str(config["quality"])+" "
    if(config["flip_horizontal"]):
        os_command = os_command + "-hf "
    if(config["flip_vertical"]):
        os_command = os_command + "-vf "

    os_command = os_command + "-h "+str(height)+\
        " -w "+str(width)+\
        " --metering " + config["metering_mode"] +\
        " -o "+file_name
    return os_command

def run_loop(base, pause, config):
    sun = Sun(config["latitude"],config["longitude"])

    print("Pause : " + str(pause))

    while True:
#        take_shot = sun.get_sunrise_time() < datetime.now(timezone.utc) < sun.get_sunset_time()
        take_shot = True ### For testing purposes at night

        if (take_shot == True):
            now = datetime.now()
            path = prepare_dir(base)

            name=str(datetime.now().year) + "_" + str(datetime.now().month).zfill(2) + "_" + str(datetime.now().day).zfill(2) + "_" + time.strftime("%H") + "_" + time.strftime("%M") +".jpg"
            print("Capturing " + name )
            file_name = base + "/" + path + "/" + name

            os_command = make_os_command(config, file_name)
            print(os_command)

            os.system(os_command)
            print("Written: " + file_name)
        else:
            print("Shot cancelled during hours of darkness")

        time.sleep(pause)

if(__name__ == '__main__'):
    if len(sys.argv) < 1:
        exit()
    else:
    	try:
            	pauseInterval = int(sys.argv[1])
            	basePath=config["base_path"]
            	run_loop(basePath,pauseInterval, config)
    	except KeyboardInterrupt:
    		print ("Cancelling take.py")
