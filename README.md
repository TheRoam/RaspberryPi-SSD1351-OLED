# RaspberryPi-SSD1351-OLED Display
![OLED2_small](https://github.com/TheRoam/RaspberryPi-SSD1351-OLED/assets/63456390/af35f47f-3db9-47b6-bc23-2eee57d6306a)

SSD1351 1.5" OLED display python script for Raspberry Pi. Currently displays:
+ Time and date
+ System stats (OS, disk usage and CPU temperature)
+ Local weather from World Meteorological Organization

Based on Adafruit sample guide:

https://learn.adafruit.com/adafruit-1-5-color-oled-breakout-board

## System config

1. Install Adafruit Circuitpython
Follow Adafruit's official guide for your display:

https://learn.adafruit.com/adafruit-1-5-color-oled-breakout-board/python-wiring-and-setup#setup-3042417

`sudo pip3 install --upgrade click setuptools adafruit-python-shell build adafruit-circuitpython-rgb-display`

If you find issues with your python version not finding a compatible circuit python, include --break-system-packages at the end. (It wont break anything, but don't get used to it...)

`sudo pip3 install --upgrade click setuptools adafruit-python-shell build adafruit-circuitpython-rgb-display --break-system-packages`

2. Wire as required to suit your needs and display pinout. My proposed SPI wiring is quite packed making it easy to design around it.

GND - GND (20)

VCC - 3V3 (17)

SCL - SPI0 SCLK (23)

SDA - SPI0 MOSI (19)

RES - GPIO 25 (22)

DC  - GPIO 24 (18)

CS  - SPI0 CEO (24)

![PI-SPI](https://github.com/TheRoam/RaspberryPi-SSD1351-OLED/assets/63456390/0c97d35c-f908-439a-baeb-160fceecd1b0)
(SPI pinout configurations from https://pinout.xyz/pinout/spi )

3. Run the script

`python3 piOLED.py &`

(**only** include the ampersand '&' to run the script in the background)

## Script config

Adjust any changes from the original configuration:

+ Weather city code:

https://worldweather.wmo.int/es/json/full_city_list.txt

+ Wiring pinout (use IO numbers/names rather than physical pin numbers)

```
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
```
