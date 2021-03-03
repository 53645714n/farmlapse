import os
import sys
import time
from datetime import datetime
#from camera import exposureCalc
from suntime import sun
from config import config

def try_to_mkdir(path):
    if os.path.exists(path) == False:
        os.makedirs(path)

def prepare_dir(base, now):
    path = str(now.year)
    try_to_mkdir(base + "/" +path)

    path = str(now.year)  + "/"  + str(now.month)
    try_to_mkdir(base + "/" +path)

#    path = str( datetime.now().year)  + "/"  + str( datetime.now().month)+"/"+ str( datetime.now().day)
#    try_to_mkdir(base + "/" +path)

#    path =  str( datetime.now().year)  + "/"  + str( datetime.now().month)+"/"+ str( datetime.now().day)+"/"+ str( datetime.now().hour)
#    try_to_mkdir(base + "/" +path)
    return path

def make_os_command(config, exposureMode , file_name):
    height = config["height"]
    width = config["width"]

    os_command = "/opt/vc/bin/raspistill -q "+str(config["quality"])+" "
    if(config["flip_horizontal"]):
        os_command = os_command + "-hf "
    if(config["flip_vertical"]):
        os_command = os_command + "-vf "

    os_command = os_command + "-h "+str(height)+\
        " -w "+str(width)+\
        " --exposure " +exposureMode +\
        " --metering " + config["metering_mode"] +\
        " -o "+file_name
    return os_command

def run_loop(base, pause, config):
    latitude = config["latitude"]
    longitude = config["longitude"]
    sun = Sun(latitude, longitude)

    current_milli_time = lambda: int(round(time.time() * 1000))

    print("Pause : " + str(pause))

    while True:
#        hoursMinutes = int(time.strftime("%H%M"))
#        exposureMode = exposureCalc1.get_exposure(hoursMinutes)
        take_shot = sun.get_sunrise_time() < datetime.now < sun.get_sunset_time()

        if (take_shot == True):
            now = datetime.now()
            path = prepare_dir(base, now)

#            time = str(hoursMinutes())
            name=path.replace("/", "_") + "_" + str( datetime.now().day) + "_" + time.strftime("%H") + "_" + time.strftime("%M") +".jpg"
            print("Capturing " + name + " in " + exposureMode + " mode")
            file_name = base + "/" + path + "/" + name

            os_command = make_os_command(config, exposureMode, file_name)
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
