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
Installing required software

Go to interfaces and enable the camera. Set the right localization and timezone while youŕe here.
Make sure your pi is up to date and all necessery packages are installed because you might not be able to access the internet with it again.
```
sudo apt-get update
sudo apt-get upgrade -y
sudo apt install python3-pip git dnsmasq hostapd npm ffmpeg -y
git clone https://github.com/53645714n/farmlapse
cd farmlapse
pip3 install suntime
sudo reboot
```
Create node.js service
```
cd farmlapse/node
npm init
```
Answer all questions (or skip them)
```
npm install express
```
Copy the service file and enble it
```
cd ..
sudo cp farmlapsehotspot.service /etc/systemd/system
sudo systemctl enable farmalpsehotspot.service
```
Make a timelapse automatically every night from all picturs in the pictures folder:
```
crontab -e
```
and add
```
0 0 * * * sh /home/pi/farmlapse/create_farmlapse.sh
```
!!! Afther the following steps you probobly won't be able to use the internet with your pi !!!

Set a static IP with dhcpd
```
sudo nano /etc/dhcpcd.conf
```
Paste the following at the end of the file
```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```
this basically gives the wireless card a static IP and tells it to ignore any wpa_supplicant files.

Configure the DHCP server with dnsmasq
```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
```
This moves the old configuration and opens a new configuration in which we will paste:
```
interface=wlan0      # Use the require wireless interface - usually wlan0
dhcp-range=192.168.4.2,192.168.4.255,255.255.255.0,15m
address=/#/192.168.4.1 # Redirect all domains (the #) to the address 192.168.4.1 (the server on the (Pi)
```

Configuring the access point
```
sudo nano /etc/hostapd/hostapd.conf
```
and paste:
```
interface=wlan0
driver=nl80211
ssid=Farmlapse
channel=7
hw_mode=g
```
This enables the wifi access point with name 'Farmlapse' in the 2.4 GHz band. 
To tell the system where to find this file:
```
sudo nano /etc/default/hostapd
```
and find/replace this line:
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
Now unmask and enable hostapd:
```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

Configuring the pi as a router
```
sudo nano /etc/sysctl.conf
```
Uncomment the line 'net.ipv4.ip_forward=1'.

Set firewall configuration:
```
sudo iptables -t nat -A  POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -t nat -I PREROUTING -d 192.168.4.1 -p tcp --dport 80 -j DNAT --to-destination 192.168.4.1:3000
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```
Tell the system where to find the iptables rules:
```
sudo nano /etc/rc.local
```
and paste the following just before 'exit 0'
```
iptables-restore < /etc/iptables.ipv4.nat
```

Configuring the node.js server

Wish list
---------
* Add exposurecalc based on actual sunrise-sunset times
* Add variables to tell the script to run only at night/day/both/day with offset
* Maybe add some logging
