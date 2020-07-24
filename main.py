from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
from framebuf import FrameBuffer, MONO_VLSB
import utime, random, gc

SCL_PIN = 22
SDA_PIN = 4
SW_PIN = 26

SCREEN_W = 128
SCREEN_H = 64
DISPLAY_BLACK = 0
DISPLAY_WHITE = 1
DELAY = 0

BLOCK_W = 5
BLOCK_H = 5
BLOCK_SPEED = 8

PILLAR_W = 4
PILLAR_H = 20
PILLAR_SPEED = 3


# create object OLED
i2c = I2C(-1,scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
display = SSD1306_I2C(SCREEN_W, SCREEN_H, i2c, 0x3c)

# setting input switch
switch = Pin(SW_PIN, Pin.IN)
gc.enable()

class Sprite:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

class Pillar(Sprite):
	def __init__(self, *args):
		super().__init__(*args)
		self.exist = True

	def setSpeed(self, speed_x):
		self.speed_x = speed_x

	def move(self):
		self.speed_x = abs(self.speed_x) * -1
		self.x += self.speed_x
		if self.x < 0:
			self.exist = False


class Block(Sprite):
	def __init__(self, *args):
		super().__init__(*args)
		self.jumping = False
		self.reachHighest = False

	def setSpeed(self, speed_y):
		self.speed_y = speed_y

	def activateJump(self):
		self.jumping = True

	def isJumping(self):
		return self.jumping

	def jump(self):
		if self.reachHighest == False:
			self.y -= abs(self.speed_y)
			if self.y < self.h:
				self.y = self.h
				self.reachHighest = True
		else:
			self.fall()

	def fall(self):
		self.y += abs(self.speed_y)
		if self.y >= SCREEN_H - self.h:
			self.y = SCREEN_H - self.h
			self.jumping = False
			self.reachHighest = False

	def isCollidedWith(self, other):
		return (other.x - self.w) < self.x < (other.x + other.w) and (other.y - self.h) < self.y < (other.y + other.h)

score = 0
score_show = True
pillars = []
block = None

def displayClear():
    display.fill(0)
    display.show()

def displayCenterText(text):
	display.fill(0)
	display.text(text, (SCREEN_W - len(text) * 8) // 2, SCREEN_H // 2)
	display.show()

def displayCenterTextOneByOne(text, delay):
    display.fill(0)
    for i in range(1, len(text) + 1):
			displayCenterText(text[:i] + ' ' * (len(text) - i))
			utime.sleep_ms(delay)
    display.show()

def resetArcade():
	global block
	global pillar
	global score
	global score_show
	score = 0
	score_show = True
	pillars.clear()
	pillars.append(Pillar((SCREEN_W - PILLAR_W), (SCREEN_H  - PILLAR_H), PILLAR_W, PILLAR_H))
	for pillar in pillars:
		pillar.setSpeed(PILLAR_SPEED)
	block = Block(BLOCK_W, (SCREEN_H - BLOCK_H - 1), BLOCK_W, BLOCK_H)
	block.setSpeed(BLOCK_SPEED)

def refreshScreen():
	global score
	global score_show
	display.fill(0)
	for pillar in pillars:
		if pillar.exist:
			display.fill_rect(pillar.x, pillar.y, pillar.w, pillar.h, DISPLAY_WHITE)
		else:
			pillars.pop(0)
			random_item = random.randint(1,2)
			if random_item == 1:
				new_pillar = Pillar((SCREEN_W - PILLAR_W), (SCREEN_H  - PILLAR_H), PILLAR_W, PILLAR_H + 20)
			elif random_item == 2:		
				new_pillar = Pillar((SCREEN_W - PILLAR_W), 0, PILLAR_W, PILLAR_H + 35)
			new_pillar.setSpeed(PILLAR_SPEED + (score//100))
			pillars.append(new_pillar)
			block.setSpeed(BLOCK_SPEED + (score//250))
	display.fill_rect(block.x, block.y, BLOCK_W, BLOCK_H, DISPLAY_WHITE)
	if score_show:
		# Display Score on top-right corner
		display.text(str(score), (SCREEN_W - len(str(score)) * 8), 0, 1)
	display.show()

score_show = False
gc.collect()
utime.sleep(0.1)
displayCenterText('Block runner')
utime.sleep(2)

while True:
	# check button pressed to start game
	while True:
		if score_show:
				displayCenterText('PRESS TO START')
		else:
				displayClear()
		score_show = not score_show
		for _ in range(10):
				if switch.value() == 1:
						break
				utime.sleep_ms(50)
		else:
				continue
		break

	# Start game
	displayCenterTextOneByOne('Ready', 100)
	utime.sleep(1)
	resetArcade()

	# Game play
	while True:
		if switch.value() == 1 and block.isJumping() == False:
			block.activateJump()

		if block.isJumping():
			block.jump()

		for pillar in pillars:
			if pillar.exist:
				pillar.move()
				break
		if block.isCollidedWith(pillars[0]):
			break
		else:
			score += 1
		refreshScreen()
		gc.collect()
		utime.sleep_ms(DELAY)

	# Game end
	displayClear()
	refreshScreen()
	utime.sleep(0.7)
	score_show = True
	refreshScreen()
	displayCenterTextOneByOne('GAME OVER', 100)

	# Display score
	utime.sleep(1.5)
	displayClear()
	utime.sleep(0.1)
	displayCenterText('SCORE: ' + str(score))
	utime.sleep(3)
	displayClear()
	score_show = False