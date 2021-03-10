farmlapse - create timelapses with your Raspberry Pi
==========

farmlapse gives you a smart way to capture photos for your timelapses. It is smart because it only takes pictures between sunrise and sunset and creates a useful folder structure. It is simple because it only depends on Python and `raspistill` both of which are normally already available and one extra library called `sunrise`.

How does it work?
------------------

Start phototimer through a terminal, `ssh` connection or `@reboot crontab` specifying the amount of seconds between photos after that. By default photos are stored in `/home/pi`, but this is configurable along with the quality level of the photos.

This is an example `config.py` file which should create files that are about 2MB in size:

```python
config = {}
config["latitude"] = 400
config["longitude"] = 2000

config["flip_horizontal"] = True
config["flip_vertical"] = False
config["metering_mode"] = "matrix"

config["base_path"] = "/home/pi"
config["height"] = 1536
config["width"] = 2048
config["quality"] = 100
```


Usage
-----
Terminal
```
$ python take.py 3600 &
```
Crontab
```
sudo crontab -e
```
and add
```
@reboot /usr/bin/python3 /home/pi/farmlapse/take.py 3600 &
```
This will takes a photo every hour between sunrise and sunset and save it in home/pi using a folder such as: /2014/11/2014_11_1_10_15.jpg (year/month/year_month_day_hour_minutes.jpg)

Installation
-----------
Enable pi camera
```
sudo raspi-config
```
Go to interfaces and enable the camera. Set the right localization and timezone while youŕe here.
Make sure your pi is up to date and all necessery packages are installed because you might not be able to access the internet with it again.
```
sudo apt update
sudo apt upgrade
sudo apt install python3-pip git dnsmasq hostapd npm
git clone https://github.com/53645714n/farmlapse
cd farmlapse
pip3 install suntime
```



Wish list
---------
* Add exposurecalc based on actual sunrise-sunset times
* Add variables to tell the script to run only at night/day/both/day with offset
* Maybe add some logging
