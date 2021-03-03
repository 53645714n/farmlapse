farmlapse - create timelapses with your Raspberry Pi
==========

farmtimer gives you a smart way to capture photos for your timelapses. It is smart because it only takes pictures between sunrise and sunset and creates a useful folder structure. It is simple because it only depends on Python and `raspistill` both of which are normally already available and one extra library called `sunrise`.

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
config["quality"] = 35
```


Usage
-----
```
$ python take.py 3600 &
```

This will takes a photo every hour and save it in home/pi using a folder such as: /2014/11/2014_11_1_10_15.jpg (year/month/year_month_day_hour_minutes.jpg)

* Designed to be run constantly.
