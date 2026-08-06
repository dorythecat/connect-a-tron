# connect-a-tron
> A connectivity software for all of my lab and test equipment

I love electronics. Since I was eight years old, electronics and programming have been my best friends, and my most consistent source of entertainment. I have always had a huge enjoyment on test equipment, because it's our way of measuring all of the wonderful physics around us.

Recently, I found myself being the proud owner of a Keithley 2000, a 6.5 digit benchtop digitalk multimeter. Alongside a Hantek DSO2C10 (Modified to be a DSO2D15 in terms of functionality), they are my "bench" (a.k.a. the equipment that's 24/7 on my desk), and I love them dearly. But I've found that I'd like to get more out of them, because otherwise I feel like I'm doing a disservice to these frankly awesome machines.

So I decided to code my own software suite, to interact with these instruments, log their data, carry out maths, statistics, noise profiles, ppm tracking, and a lot more of stuff.

# Objectives
There are various things I want this suite to be able to do. It should run on a Raspberry Pi 4B, which is the hardware that will be tucked behind all the equipment, and connected to my LAN, so that I can access most, if not all of its functions, through a web interface.

Since I've only got two devices I wanna hook up (for now, more will hopefully come later), that's all I wanna cover for now. It will have the Keithley connected through a USB to RS232 adapter, and the Hantek will be connected directly by USB.

## Keithley 2000
The Keithley 2000 is a precision instrument, but it's also useful as a general measurement device. I mainly want to automate testing with it for the following reasons:
- Logging measurements, both one-time, and periodic
- Taking very precise measurements through averaging
- Measuring drift of voltage sources
- Measuring the effects of various external influences on various devices
- Measuring current consumption of various devices

## Hantek DSO2D15 (Originally a DSO2C10)
The Hantek DSO2C10 I have modified to be a DSO2D15 is a 150MHz, 1GSa/s, 2-channel oscilloscope, with a pretty good 1-channel AWG connected to it. Whilst it isn't an RF generator, it is still pretty accurate, and allows for a lot of possibilities. It also lacks any kind of included frequency response generator, and its FFT kinda sucks. I'd like to automate testing with it for the following reasons:
- Logging measurements, both one-time, and periodic
- Generating FFT and frequency response graphs
- Replaying captured waveforms

## Joint measurements
There is also the very inviting offer of doing some "joint measurements", that is to say, using various tools in a coordinated manner to compare measurements, carry out calibrations using one of the tools as a reference, or other similar endeavours.

# Settings format
There is (currently) one settings file, which you can find as `backend/settings.json`. This file contains definitions for the settings of what devices are available internally. That is, the devices that are physically connected to the device that is running the backend.

Every device supported is included on the file. You can deactivate any of these devices by either removing that section, or setting the value of their `enabled` value to `false`. All devices have the `port` setting, which indicates which port of the machine the device is connected to.

# Testing it out
You can test out the web at http://89.141.111.112:8001 and the API at http://89.141.111.112:8000

# Setting it up
To set up your own instance of connect-a-tron, simply clone the repo. Make sure your system has the ability to run a [FastAPI program](https://github.com/fastapi/fastapi) and then go ahead and execute `python -m fastapi run backend/api.py --port 8000`, and the API will now be available on port 8000 of your machine. For the web, set up your machine to run a PHP server with `web/index.php` as the index. That should do it!

If you're on Windows, a quick setup script for your delight, that automatically starts the API (requires git and python to be installed, I'm not a magician):
```
git clone https://github.com/dorythecat/connect-a-tron
cd connect-a-tron
python -m pip install "fastapi[standard]"
python -m fastapi run backend/api.py --port 8000
```
Then go to `http://localhost:8000` on your browser, and ta-dah! :D
