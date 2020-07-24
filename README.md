# Block-runner Micropython Game on ESP32
### Prerequired
- [Install esptool.py](https://github.com/espressif/esptool/)
- [Donwload and Install ESP32 Micropython firmware](https://micropython.org/download/esp32/)
- [Install ampy](https://pypi.org/project/adafruit-ampy/)
- [Download ssd1306 library for Micropython](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py)

### How to Setup & Install game
- Connect SSD1306 OLED with ESP32 (SDA= GPIO4, SCL= GPIO22)
- Connect switch to GPIO25
- Put ssd1306 library to ESP32 by using	`ampy --port PORT put ssd1306.py`
- Put main.py (game file) to ESP32 by using `ampy --port PORT put main.py`
- Reset ESP32 and enjoy the game !!!

> If you change GPIO that connected to SSD13006 OLED and switch, you must change GPIO number in main.py (game file) too.