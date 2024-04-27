# Based on original sample script by Adafruit:
# https://learn.adafruit.com/adafruit-1-5-color-oled-breakout-board/python-usage
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Adapted by THE ROAMING WORKSHOP 2024

"""
This will show some Linux Statistics on the attached display. Be sure to adjust
to the display you have connected. Be sure to check the learn guides for more
usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341
from adafruit_rgb_display import st7789  # pylint: disable=unused-import
from adafruit_rgb_display import hx8357  # pylint: disable=unused-import
from adafruit_rgb_display import st7735  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1351  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1331  # pylint: disable=unused-import

#Additional libraries for WMO weather
import datetime
import requests

#CityID from WMO City list:
#https://worldweather.wmo.int/es/json/full_city_list.txt
CityID="1238"

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Configuration for CS and DC pins (adjust to your wiring):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D24)
reset_pin = digitalio.DigitalInOut(board.D25)

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = ssd1351.SSD1351(spi, rotation=270,                         # 1.5" SSD1351
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# First define some constants to allow easy positioning of text.
padding = -2
x = 0

# Load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
#   --> Not really, just point to the right /usr/.. directory
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#fontDir="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
fontDir="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
#fontDir="/usr/share/fonts/truetype/noto/NotoMonoRegular.ttf"

# Set different font sizes (you could also define different font files)
font = ImageFont.truetype(fontDir, 14)
fontB = ImageFont.truetype(fontDir, 11)
fontC = ImageFont.truetype(fontDir, 22)

# Dimensions used to adjust 80x60 original weather icons
scaled_width=int(80*0.6)
scaled_height=int(60*0.6)

#set hour to 0 at start so it's refreshed
hour_count=0

# Refresh loop
while True:
    # Define commands to display system data
    # -System OS
    cmd = 'cat /etc/os-release | head -n 1 | cut -d \'"\' -f 2'
    OS = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # -Disk usage
    cmd = 'df -h | awk \'$NF=="/"{printf "D %d/%d GB", $3,$2}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    # -CPU Temperature
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"T %.1f ºC\", $(NF-0) / 1000}'"
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    #Get time and date
    D = datetime.datetime.now()
    DATE=D.strftime("%d")+" "+D.strftime("%B")+" "+D.strftime("%Y") # d - Month - YYYY
    TIME=D.strftime("%X") # hh:mm

	#update current hour
    if hour_count != int(D.strftime("%H")):
        hour_count=int(D.strftime("%H"))
        #get weather when hour change
        try:
            w_data=requests.get("https://worldweather.wmo.int/en/json/"+CityID+"_en.json").json()["city"]["forecast"]["forecastDay"][0]
            CITY=requests.get("https://worldweather.wmo.int/en/json/"+CityID+"_en.json").json()["city"]["cityName"]
            tMIN=requests.get("https://worldweather.wmo.int/en/json/"+CityID+"_en.json").json()["city"]["forecast"]["forecastDay"][0]["minTemp"]
            tMAX=requests.get("https://worldweather.wmo.int/en/json/"+CityID+"_en.json").json()["city"]["forecast"]["forecastDay"][0]["maxTemp"]
            #weather icon
            w_ico=int(str(w_data["weatherIcon"])[:-2])
            #check day/night icons
            if (hour_count >= 6 and hour_count < 20) and (w_ico > 20 and w_ico < 25):
                w_ico=str(w_ico)+"a.png"
            elif (hour_count < 6 or hour_count >= 20) and (w_ico > 20 and w_ico < 25):
                w_ico=str(w_ico)+"b.png"
            else:
                w_ico=str(w_ico)+".png"
        except:
	    #Exception for startup connextion errors
            w_ico="28.png"
            CITY="------"
            tMIN="--"
            tMAX="--"

    # Set weather icon file
    image = Image.open("/home/piÑa/Documents/TheCloud/wmo-img/"+w_ico)
    # Scale the image to the smaller screen dimension
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # I tried to place the icon somewhere else but fails
    #image=image.rotate(0, translate=(15, 0))

    bg=Image.new("RGB", (width, height))
    # Draw a black filled box to clear the image.
    draw = ImageDraw.Draw(bg)
    draw.rectangle([0, 0, width, height], outline=0, fill=None)

    # Write text.
    y = padding
    #Display time
    draw.text((x+13, y), TIME, font=fontC, fill="#00FFFF") #FFFF00
    y += fontC.getbbox(TIME)[3]+3
    #Display date
    draw.text((x+10, y), DATE, font=font, fill="#FFFFFF")
    y += font.getbbox(DATE)[3]+3
    #Display OS
    draw.text((x, y), OS, font=fontB, fill="#FF6699")
    y += fontB.getbbox(OS)[3]
    #Display disk space
    draw.text((x, y), Disk, font=font, fill="#99FF99")
    y += font.getbbox(Disk)[3]
    draw.text((x, y), Temp, font=font, fill="#FFCCCC")
    y += font.getbbox(Temp)[3]+5
    #Display city
    draw.text((scaled_width, y), CITY, font=font, fill="#FFFFFF")
    y += font.getbbox(CITY)[3]+5
    #Display min/max temperature
    draw.text((50, y), tMIN, font=fontC, fill="#0000FF")
    draw.text((76, y), "/", font=fontC, fill="#FFFFFF")
    draw.text((88, y), tMAX, font=fontC, fill="#FF0000")

    #Show on display
    disp.image(bg)
    disp.image(image)
    #Sleep for 1 second
    time.sleep(1)

